import logging

from utils import (
    config,
    db,
    log,
)
from services import system

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


DEBUG = config.DEBUG
logger = logging.getLogger()
log.setup()
serve = FastAPI(default_response_class=ORJSONResponse, debug=DEBUG)


@serve.on_event("startup")
async def startup():
    await db.start()
    await system.initialize()
    logger.debug("initialized")


@serve.on_event("shutdown")
async def shutdown():
    await db.stop()
