# noqa
import gevent.monkey

from slagents import settings
from slagents.main import app

# gevent.monkey.patch_all()
import grpc.experimental.gevent as grpc_gevent

# grpc_gevent.init_gevent()
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.get("PORT", 5001), debug=True)
