from falcon import asgi, media
from pymongo import MongoClient
from bson.json_util import dumps, loads


from .endpoints.drivers.collection import DriversCollection
from .config import Config

class Base:
    async def on_get(self, req, res):
        res.media = {'hello': 'world'}


def create_app(config=None, mongodb=None):
    config = config or Config()
    mongodb = mongodb or MongoClient(config.mongodb_url)

    drivers_collection = DriversCollection(mongodb)
    app = asgi.App()
    app.add_route('/', Base())
    app.add_route('/drivers', drivers_collection)
    app.add_route('/drivers/truck', drivers_collection, suffix='truck')
    app.add_route('/drivers/unloaded', drivers_collection, suffix='unloaded')
    extra_handlers = {
        'application/json': media.JSONHandler(dumps=dumps, loads=loads)
    }

    app.req_options.media_handlers.update(extra_handlers)
    app.resp_options.media_handlers.update(extra_handlers)

    return app

app = create_app()