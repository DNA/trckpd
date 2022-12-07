import falcon
from falcon import Request, Response
from pymongo import MongoClient

class Terminal:
    def __init__(self, mongodb: MongoClient):
        self.terminal = mongodb.terminal


    async def on_get(self, req: Request, res: Response):
        res.media = self.terminal.find()


    async def on_post(self, req: Request, res: Response):
        params = await req.media
        id = self.terminal.insert_one(params).inserted_id

        driver = self.terminal.aggregate([
            { "$match": { "_id": id } },
            {
                "$lookup": {
                    "from": "drivers",
                    "localField": "driver",
                    "foreignField": "_id",
                    "as": "driver"
                }
            },
            {
                "$addFields": {
                    "driver": { "$arrayElemAt": ["$driver", 0] }
                }
            }
        ])

        res.media = driver.next()
        res.status = falcon.HTTP_201


    async def on_get_stats(self, req: Request, res: Response):
        stats = self.terminal.aggregate([
            {
                "$facet": {
                    "months": [{
                        "$group": {
                            "_id": {
                                "year": { "$year": "$arrived_at" },
                                "month": { "$month": "$arrived_at" }
                            },
                            "total": { "$sum": 1 }
                        },
                        "$project": {
                            "_id": {
                                "$concat": ["$_id.year", "-", "$_id.month"]
                            },
                            "total": 1
                        }

                    }],
                    "weeks": [{
                        "$group": {
                            "_id": {
                                "year": { "$year": "$arrived_at" },
                                "week": { "$week": "$arrived_at" }
                            },
                            "total": { "$sum": 1 }
                        },
                        "$project": {
                            "_id": {
                                "$concat": ["$_id.year", "-", "$_id.week"]
                            },
                            "total": 1
                        }
                    }],
                    "days": [{
                        "$group": {
                            "_id": {
                                "year": { "$year": "$arrived_at" },
                                "month": { "$month": "$arrived_at" },
                                "day": { "$dayOfMonth": "$arrived_at" }
                            },
                            "total": { "$sum": 1 }
                        },
                        "$project": {
                            "_id": {
                                "$concat": ["$_id.year", "-", "$_id.month", "-", "$_id.day"]
                            },
                            "total": 1
                        }
                    }]
                }
            }
        ])

        res.media = stats.next()


    async def on_get_trucklist(self, req: Request, res: Response):
        driver = self.terminal.aggregate([
            { "$match": { "destination": False } },
            {
                "$lookup": {
                    "from": "drivers",
                    "localField": "driver",
                    "foreignField": "_id",
                    "as": "driver"
                }
            },
            {
                "$addFields": {
                    "driver": { "$arrayElemAt": ["$driver", 0] }
                }
            }
        ])

        res.media = driver




