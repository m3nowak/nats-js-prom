FROM docker.io/library/python:3.11 as build
RUN pip install pdm
COPY pdm.lock pyproject.toml README.md /app/
COPY src /app/src
WORKDIR /app
RUN pdm build

FROM docker.io/library/python:3.11
COPY --from=build /app/dist/*.whl /tmp/
RUN pip install /tmp/*.whl
EXPOSE 8080
ENTRYPOINT [ "nats-js-prom" ]