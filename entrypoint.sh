#!/usr/bin/env bash
#!/bin/sh

poetry run uvicorn --host 0.0.0.0 --port 8001 main:app --reload

exec "$@"
