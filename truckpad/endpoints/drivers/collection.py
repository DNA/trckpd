import falcon
from falcon import Request, Response
from pymongo import MongoClient

class DriversCollection:
    def __init__(self, mongodb: MongoClient):
        self.drivers = mongodb.drivers

    async def on_get(self, req: Request, res: Response):
        res.media = self.drivers.find()


    async def on_post(self, req: Request, res: Response):
        params = await req.media
        id = self.drivers.insert_one(params).inserted_id

        res.media = self.drivers.find_one({ "_id": id })
        res.status = falcon.HTTP_201


    async def on_get_truck(self, req: Request, res: Response):
        res.media = self.drivers.find({ "has_vehicle": True })


    async def on_get_unloaded(self, req: Request, res: Response):
        res.media = self.drivers.find({ "is_loaded": False })
