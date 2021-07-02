FROM python:3.9-slim as build

RUN apt update \
    && apt install -y --no-install-recommends build-essential apt-utils \
       procps gettext wget

RUN pip install poetry
RUN poetry config virtualenvs.create false

ENV LIB_KAFKA_VERSION 1.5.2
RUN mkdir -p /opt/ \
    && cd /opt/ \
    && wget https://github.com/edenhill/librdkafka/archive/v$LIB_KAFKA_VERSION.tar.gz \
    && tar -zxvf v$LIB_KAFKA_VERSION.tar.gz \
    && cd librdkafka-$LIB_KAFKA_VERSION \
    && ./configure --install-deps \
    && make \
    && make install \
    && ldconfig

WORKDIR /app
ADD poetry.lock pyproject.toml ./
COPY .docker/entrypoint.sh /usr/local/bin/

# prod target
FROM build AS prod
RUN poetry install --no-dev

RUN pip install uwsgi ddtrace

COPY . .
RUN rm -rf /root/.cache/
# use CMD for env
CMD ["entrypoint.sh"]

# dev target
FROM build AS dev

RUN apt install -y vim

RUN poetry install
COPY . .
