FROM python:3.12-slim as base

ENV GUNICORN_VERSION=23.0.0

WORKDIR /app

COPY requirements.txt ./
RUN pip install gunicorn==$GUNICORN_VERSION && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

COPY src/ ./

FROM base AS app

ENTRYPOINT ["gunicorn"]

FROM base AS test

ENV PYTEST_VERSION=8.3.3

RUN pip install pytest==$PYTEST_VERSION && \
    rm -rf /root/.cache/pip

COPY ./tests ./tests

CMD ["pytest", "tests/"]
