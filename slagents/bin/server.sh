#!/bin/bash

set -e


# Start Gunicorn
gunicorn --timeout=0 --keep-alive=30 --pythonpath=/code/Gentopia --worker-class=gevent -w=3 --worker-connections=300  --bind=0.0.0.0:5000 --log-level=info slagents.wsgi:app
