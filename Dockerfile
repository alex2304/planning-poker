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
RUN pip install pytest
COPY ./tests ./tests
CMD ["pytest", "tests/"]
