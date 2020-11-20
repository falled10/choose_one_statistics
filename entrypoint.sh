#!/usr/bin/env bash
#!/bin/sh

poetry run gunicorn main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --workers=4 --log-level=info

exec "$@"
