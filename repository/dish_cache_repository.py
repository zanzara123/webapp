from redis import Redis
from schema import DishSchema

import json

class CacheDishRepository:
    def __init__(self, redis: Redis):
        self.redis = redis


    async def get_all_dishes(self) -> list[DishSchema]:
        async with self.redis as redis:
            dishes_json = await redis.lrange("dish", 0, -1)

            return [DishSchema.model_validate(json.loads(d)) for d in dishes_json]



    async def set_dishes(self, dishes: list[DishSchema]):
        if not dishes:
            return
        
        dishes_json: list[str] = [d.model_dump_json() for d in dishes]

        async with self.redis as redis:
            await redis.delete("dish")
            await redis.lpush("dish", *dishes_json)

