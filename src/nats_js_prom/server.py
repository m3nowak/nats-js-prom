import asyncio

import nats.aio.client
import nats.js.api
from litestar import Litestar, get
from litestar.datastructures import ResponseHeader, State

from nats_js_prom import config


@get('/', response_headers=[ResponseHeader(name='Content-Type', value='text/plain; version=0.0.4')])
async def metrics_handler(state: State) -> str:
    nc: nats.aio.client.Client = state.nc
    cfg: config.Config = state.cfg
    js = nc.jetstream(domain=cfg.stream_domain)
    cons = await js.add_consumer(cfg.stream_name, nats.js.api.ConsumerConfig(inactive_threshold=10))
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
                ret.append(f'{label} {value}')
            except ValueError:
                print(f'Failed to parse {msg.data} as float')
            finally:
                acks.append(msg.ack())
        await asyncio.gather(*acks)
    await js.delete_consumer(cfg.stream_name, cons.name)
    return '\n'.join(ret)

async def setup_nats(app: Litestar) -> None:
    """Setup NATS connection and add it to the app state"""
    print("I am making a new connection!")
    cfg = app.state.cfg
    nc = await nats.connect(cfg.nats_url, user_credentials=cfg.nats_creds_path)
    app.state.nc = nc

async def close_nats(app: Litestar) -> None:
    """Close NATS connection"""
    print("I am closing the connection!")
    await app.state.nc.close()

def create_app(cfg: config.Config) -> Litestar:
    app = Litestar(route_handlers=[metrics_handler],
        debug=cfg.debug, on_startup=[setup_nats],
        on_shutdown=[close_nats],
        state=State({"cfg": cfg}))

    return app
