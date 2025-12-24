from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.logger import setup_logging
from backend.middleware import setup_middleware


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title='TgWebAppTest'
    )
    setup_middleware(app)
    app.mount("/static", StaticFiles(directory="webapp"), name="static")


    return app
