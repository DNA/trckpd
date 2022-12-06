from pymongo import MongoClient
from bson import ObjectId

class DriversEntity:
    def __init__(self, mongodb: MongoClient):
        self.drivers = mongodb.drivers

    async def on_get(self, req, res, id):
        res.media = self.drivers.find_one({ "_id": id })


    async def on_patch(self, req, res, id):
        self.drivers.update_one({ "_id": id }, { "$set": await req.media })
        res.media = self.drivers.find_one({ "_id": id })
