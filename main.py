import logging

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi_route_logger_middleware import RouteLoggerMiddleware

from router import social_market_router

gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
if __name__ != "__main__":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI()

app.add_middleware(RouteLoggerMiddleware)

app.include_router(
    social_market_router.router,
    prefix="/api/v1/social-market",
    tags=["Social Market Data"],
)
