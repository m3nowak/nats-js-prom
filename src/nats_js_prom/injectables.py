from dataclasses import dataclass
from typing import Generator

import nats
import prometheus_client as prom
from litestar.di import Provide

from nats_js_prom import config


@dataclass
class Metrics():
    registry: prom.CollectorRegistry


def generate_metrics_provide() -> Provide:
    def provide_metrics() -> Metrics:
        registry = prom.CollectorRegistry()
        return Metrics(registry=registry
                       )
    return Provide(provide_metrics, sync_to_thread=True, use_cache=True)


def generate_config_provide(cfg: config.Config) -> Provide:
    def provide_config():
        return cfg
    return Provide(provide_config, sync_to_thread=True, use_cache=True)


def generate_nats_provide(cfg: config.Config) -> Provide:
    async def provide_nats_connection():
        extra_params = {}
        if cfg.nats_creds_path:
            extra_params['user_credentials'] = cfg.nats_creds_path
        nc = await nats.connect(cfg.nats_url, **extra_params)
        yield nc
        await nc.close()
    return Provide(provide_nats_connection)
