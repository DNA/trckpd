from falcon import asgi, media
from pymongo import MongoClient
from bson.json_util import dumps, loads

from .config import Config

class Base:
    async def on_get(self, req, res):
        res.media = {'hello': 'world'}


def create_app(config=None, mongodb=None):
    config = config or Config()
    mongodb = mongodb or MongoClient(config.mongodb_url)

    app = asgi.App()
    app.add_route('/', Base())
    extra_handlers = {
        'application/json': media.JSONHandler(dumps=dumps, loads=loads)
    }

    app.req_options.media_handlers.update(extra_handlers)
    app.resp_options.media_handlers.update(extra_handlers)

    return app

app = create_app()