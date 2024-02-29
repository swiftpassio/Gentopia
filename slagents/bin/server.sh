#!/bin/bash

set -e


# Start Gunicorn
gunicorn --timeout=0 --keep-alive=30 --pythonpath=/code/Gentopia --worker-class=gevent -w=3 --worker-connections=100  --bind=0.0.0.0:8080 --log-level=info slagents.wsgi:app
