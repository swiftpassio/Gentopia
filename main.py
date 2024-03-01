import logging
from contextlib import asynccontextmanager

import firebase_admin
from fastapi import FastAPI
from starlette.responses import JSONResponse

import swiftlane.api.zendesk.router
from swiftlane import settings
from swiftlane.utilities import http_client

logging.basicConfig(level=logging.INFO)

API_PREFIX = "/agents"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if len(firebase_admin._apps) == 0:
        firebase_admin.initialize_app(
            name="swiftlane-dev-instance",
            options={
                "projectId": "swiftlane-dev",
                "serviceAccountId": settings.SERVICE_ACCOUNTS_FOR_CLOUD_TASK_HANDLER,
            },
        )
    await http_client.initialize_session()
    try:
        yield
    finally:
        await http_client.close_session()


app = FastAPI(
    lifespan=lifespan,
    title="SL AI Agents API",
    description="cloud run-based microservice for handling all logic related to ai agents integrations.",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.include_router(
    swiftlane.api.zendesk.router.router, prefix=API_PREFIX, tags=["Zendesk Support Bot"]
)


@app.get(f"{API_PREFIX}/ping")
async def ping():
    return JSONResponse({"pong": True})
