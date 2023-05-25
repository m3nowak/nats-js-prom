# nats-js-prom

NATS JetStream data exporter for Prometheus

It exports data in stream itself, not NATS metadata. Works only with stream where messeges are limited to 1 per subject

Config example:
```yaml
natsCredsPath: 'app.creds'
natsUrl: '192.168.4.23:4222'
httpPort: 8080
httpHost: '0.0.0.0'
streamName: 'stream-test'
streamDomain: 'home-domain'
exportPrefix: 'home_automation'
valueMapping:
  'close': 0
  'open': 1
  'off': 0
  'on': 1
  'false': 0
  'true': 1
  
```
