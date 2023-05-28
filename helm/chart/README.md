# nats-js-prom

NATS JetStream data exporter for Prometheus. Written in Python3.

Exports data in stream itself, not NATS metadata. Works only with streams where messeges are limited to 1 per subject.

## Installation
```sh
helm install nats-js-prom oci://ghcr.io/m3nowak/helm/nats-js-prom --values values.yaml
```

## Config

| Key | Description | Default |
| --- | --- | --- |
| `config.streamDomain` | name of stream domain, if needed | `null` |
| `config.streamName` | name of stream, required | `null` |
| `config.valueMapping` | mapping of text values to numeric values | `{}` |
| `config.natsUrl` | nats server url | `nats://localhost:4222` |
| `config.exportPrefix` | prefix for prom metrics | `null` |
| `config.debug` | enable debug mode | `false` |
| `config.creds.secretName` | secret name | `null` |
| `config.creds.secretKey` | secret key | `null` |
| `deployment.image` | image to use | `ghcr.io/m3nowak/nats-js-prom:latest` |
| `monitor.enabled` | whether to enable pod monitor | `true` |
| `monitor.extraLabels` | extra labels for pod monitor | `{}` |


### Example
```yaml
config:
  streamDomain: 'domain'
  streamName: 'stream-name'
  valueMapping:
    'on': 1
    'off': 0
  natsUrl: 'nats://nats-svc.nats:4222'
  exportPrefix: 'nats_import'
  debug: false
  creds:
    secretName: nats-creds
    secretKey: nats.creds
deployment:
  image: ghcr.io/m3nowak/nats-js-prom:latest
monitor:
  enabled: true
  extraLabels:
    release: prometheus

```
