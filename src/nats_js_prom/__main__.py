

import asyncio

import click
import uvicorn

from nats_js_prom import config, server


@click.command("nats-js-prom")
@click.option("--config", "-c", type=click.Path(exists=True, readable=True), required=True)
def main(config: str):
    asyncio.run(async_main(config))


async def async_main(config_path: str):
    cfg = await config.get_config(config_path)
    print('Starting server...')
    uv_app = server.create_app(cfg)
    uv_config = uvicorn.Config(uv_app, host=cfg.http_host, port=cfg.http_port)
    uv_server = uvicorn.Server(uv_config)
    await uv_server.serve()


if __name__ == '__main__':
    main()
