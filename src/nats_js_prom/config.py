import aiofiles
import humps
import yaml
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class BaseModel(PydanticBaseModel):
    '''Base configuration model with camelCase fields'''
    class Config:
        allow_population_by_field_name = True
        alias_generator = humps.camelize


class Config(BaseModel):
    nats_creds_path: str | None
    nats_url: str
    export_prefix: str | None
    stream_name: str
    stream_domain: str | None
    http_port: int = Field(default=8080)
    http_host: str = Field(default='0.0.0.0')
    value_mapping: dict[str, float] = Field(default_factory=dict)

async def get_config(path):
    async with aiofiles.open(path, mode='r') as f:
        config_raw = yaml.safe_load(await f.read())
        return Config(**config_raw)
