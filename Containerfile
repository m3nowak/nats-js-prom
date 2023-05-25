FROM docker.io/library/python:3.11 as build
RUN pip install pdm
COPY . /app
WORKDIR /app
RUN pdm build

FROM docker.io/library/python:3.11
COPY --from=build /app/dist/*.whl /tmp/
RUN pip install /tmp/*.whl
EXPOSE 8080
ENV CONF_PATH = /etc/nats-js-prom.yaml
CMD ["nats-js-prom", "-c", "${CONF_PATH}"]