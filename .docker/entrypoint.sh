#!/usr/bin/env bash
set -euo pipefail

main() {
    config
    exec ddtrace-run uwsgi --ini /app/.docker/uwsgi.ini
}

config() {
    # pod init
    if [ "$MODE" = "web" ]; then
      /bin/bash -c "python manage.py collectstatic --noinput"
    fi
}

main "$@"
