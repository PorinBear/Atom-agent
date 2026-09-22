#!/usr/bin/env bash
set -euo pipefail
uvicorn server:app --host 0.0.0.0 --port "${PORT:-8000}" &
exec python agent.py --worker
