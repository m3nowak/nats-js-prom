# nats-js-prom

NATS JetStream data exporter for Prometheus. Written in Python3.

Exports data in stream itself, not NATS metadata. Works only with streams where messeges are limited to 1 per subject.

## CLI

Building (Requires PDM):
```sh
pdm build
```

Installation:
```sh
pip install dist/nats_js_prom-*.whl
```

Running:
```sh
nats-js-prom -c config/path.yaml
```

Example config file:
```yaml
natsCredsPath: 'app.creds' # path to nats credentials file
natsUrl: '192.168.0.128:4222' # nats server URL
httpPort: 8080 # http port to listen on
httpHost: '0.0.0.0' # http host to listen on
streamName: 'stream-test' # scraped nats stream name
streamDomain: 'home-domain' # optional NATS domain
exportPrefix: 'home_automation' # export prefix for stats
valueMapping: # value mappings for text values
  'close': 0
  'open': 1
  'off': 0
  'on': 1
  'false': 0
  'true': 1
  
```

## Containers

Supported architectures:
 - AMD64 (aka x64, x86_64)
 - ARM64

Running as a container:
```sh
docker run -v /path/to/cfg/dir:/cfg ghcr.io/m3nowak/nats-js-prom:latest -c /cfg/path.yaml
```

## Helm
See below

[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/nats-js-prom)](https://artifacthub.io/packages/search?repo=nats-js-prom)

