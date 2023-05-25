import asyncio
from datetime import datetime

import nats.aio.client
import nats.js.api
import prometheus_client as prom
from litestar import Litestar, get
from litestar.datastructures import ResponseHeader

from nats_js_prom import config, injectables


@get('/', response_headers=[ResponseHeader(name='Content-Type', value='text/plain; version=0.0.4')])
async def hello_world(metrics: injectables.Metrics, nc: nats.aio.client.Client, cfg: config.Config) -> str:
    js = nc.jetstream(domain=cfg.stream_domain)
    cons = await js.add_consumer(cfg.stream_name, nats.js.api.ConsumerConfig(inactive_threshold=120))
    # str = await js.stream_info(cfg.stream_name)
    sub = await js.pull_subscribe('', cons.name, cfg.stream_name)
    pending = cons.num_pending or 0
    ret = []
    for _ in range(pending):
        msgs = await sub.fetch(1)
        acks = []
        for msg in msgs:
            try:
                to_parse = msg.data.decode('utf-8')
                if to_parse in cfg.value_mapping:
                    to_parse = cfg.value_mapping[to_parse]
                value = float(to_parse)
                label = msg.subject.replace('.', '_').replace('-', '_')
                if cfg.export_prefix:
                    label = f'{cfg.export_prefix}_{label}'
                ts = msg.metadata.timestamp or datetime.now()
                ret.append(f'{label} {value} {int(ts.timestamp())}')
            except ValueError:
                print(f'Failed to parse {msg.data} as float')
            finally:
                acks.append(msg.ack())
        await asyncio.gather(*acks)

    return '\n'.join(ret)


@get('/metrics', response_headers=[ResponseHeader(name='Content-Type', value='text/plain; version=0.0.4')])
async def metrics(metrics: injectables.Metrics) -> str:
    return prom.generate_latest(registry=metrics.registry).decode('utf-8')


def create_app(cfg: config.Config) -> Litestar:
    app = Litestar(route_handlers=[hello_world, metrics], dependencies={
        'nc': injectables.generate_nats_provide(cfg),
        'metrics': injectables.generate_metrics_provide(),
        'cfg': injectables.generate_config_provide(cfg)
    })

    return app
