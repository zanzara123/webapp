from dataclasses import dataclass

from repository import DishRepository, CacheDishRepository
from schema import DishSchema


@dataclass
class DishService:
    dish_repository: DishRepository
    dish_cache: CacheDishRepository


    def get_all_dishes(self) -> list[DishSchema]:
        if dishes := self.dish_cache.get_all_dishes():
            return dishes
        
        else:
            dishes = self.dish_repository.get_all_dishes()
            dishes_schemas = [DishSchema.model_validate(d) for d in dishes]
            self.dish_cache.set_dishes(dishes_schemas)
        
            return dishes_schemas