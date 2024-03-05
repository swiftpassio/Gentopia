#!/bin/bash

set -e


# Start Gunicorn
gunicorn --timeout=0 --keep-alive=30 --pythonpath=/code/agents --worker-class=uvicorn.workers.UvicornWorker -w=3 --worker-connections=100  --bind=0.0.0.0:8080 --log-level=info main:app

