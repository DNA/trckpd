import os

from falcon import asgi, media, routing
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps, loads

from .endpoints.drivers.collection import DriversCollection
from .endpoints.drivers.entity import DriversEntity
from .endpoints.terminal import Terminal

class Server():
    DEFAULT_MONGODB_URL = 'mongodb://localhost:27017'

    EXTRA_HANDLERS = {
        'application/json': media.JSONHandler(dumps=dumps, loads=loads)
    }

    class ObjectIdConverter(routing.BaseConverter):
        def convert(self, value):
            return ObjectId(value)

    def __init__(self, mongodb=None):
        mongodb_url = os.environ.get('MONGODB_URL', self.DEFAULT_MONGODB_URL)

        self.mongodb = mongodb or MongoClient(mongodb_url)
        self.app = asgi.App()
        
    def add_media_handlers(self):
        self.app.req_options.media_handlers.update(self.EXTRA_HANDLERS)
        self.app.resp_options.media_handlers.update(self.EXTRA_HANDLERS)

    def add_converters(self):
        self.app.router_options.converters.update({ 'ObjectId': self.ObjectIdConverter })

    def add_routes(self):
        drivers_collection = DriversCollection(self.mongodb)
        drivers_entity = DriversEntity(self.mongodb)

        self.app.add_route('/drivers', drivers_collection)
        self.app.add_route('/drivers/truck', drivers_collection, suffix='truck')
        self.app.add_route('/drivers/unloaded', drivers_collection, suffix='unloaded')
        self.app.add_route('/drivers/{id:ObjectId}', drivers_entity)
        self.app.add_route('/terminal', Terminal(self.mongodb))
        self.app.add_route('/terminal/stats', Terminal(self.mongodb), suffix='stats')
        self.app.add_route('/terminal/trucklist', Terminal(self.mongodb), suffix='trucklist')


    def create(self):
        self.add_media_handlers()
        self.add_converters()
        self.add_routes()

        return self.app
