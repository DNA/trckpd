import falcon.asgi
import logging

from pymongo import MongoClient

from .config import Config

class Base:
    async def on_get(self, req, res):
        res.media = {'hello': 'world'}


def create_app(config=None, mongodb=None):
    config = config or Config()
    mongodb = mongodb or MongoClient(config.mongodb_url)

    app = falcon.asgi.App()
    app.add_route('/', Base())
    app.add_route('/drivers', Drivers())

    return app

app = create_app()