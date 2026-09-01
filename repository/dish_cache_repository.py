from redis import Redis
from schema import DishSchema

import json

class CacheDishRepository:
    def __init__(self, redis: Redis):
        self.redis = redis


    def get_all_dishes(self) -> list[DishSchema]:
        with self.redis as redis:
            dishes_json = redis.lrange("dish", 0, -1)

            dishes = [DishSchema.model_validate(json.loads(d)) for d in dishes_json]

            return dishes




    def set_dishes(self, dishes: list[DishSchema]):
        if not dishes:
            return

        dishes_json: list[str] = [d.model_dump_json() for d in dishes] 

        with self.redis as redis:
            redis.delete("dish")
        
            redis.lpush("dish", *dishes_json)

