from falcon import asgi, media, routing
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps, loads


from .endpoints.drivers.collection import DriversCollection
from .endpoints.drivers.entity import DriversEntity
from .config import Config

class Base:
    async def on_get(self, req, res):
        res.media = {'hello': 'world'}

class ObjectIdConverter(routing.BaseConverter):
    def convert(self, value):
        return ObjectId(value)


def create_app(config=None, mongodb=None):
    config = config or Config()
    mongodb = mongodb or MongoClient(config.mongodb_url)

    drivers_collection = DriversCollection(mongodb)
    drivers_entity = DriversEntity(mongodb)

    app = asgi.App()
    extra_handlers = {
        'application/json': media.JSONHandler(dumps=dumps, loads=loads)
    }

    app.req_options.media_handlers.update(extra_handlers)
    app.resp_options.media_handlers.update(extra_handlers)
    app.router_options.converters.update({ 'ObjectId': ObjectIdConverter })

    app.add_route('/', Base())
    app.add_route('/drivers', drivers_collection)
    app.add_route('/drivers/truck', drivers_collection, suffix='truck')
    app.add_route('/drivers/unloaded', drivers_collection, suffix='unloaded')
    app.add_route('/drivers/{id:ObjectId}', drivers_entity)

    return app

app = create_app()