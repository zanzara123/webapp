from dataclasses import dataclass

from repository import DishRepository, CacheDishRepository
from schema import DishSchema, DishCreateSchema

from exception import DishNotFound


@dataclass
class DishService:
    dish_repository: DishRepository
    dish_cache: CacheDishRepository

    # auth_service: Aut


    async def get_all_dishes(self) -> list[DishSchema]:
        if cache_dishes := await self.dish_cache.get_all_dishes():
            return cache_dishes

        else:
            dishes = await self.dish_repository.get_all_dishes()
            dishes_schemas = [DishSchema.model_validate(d) for d in dishes]
            await self.dish_cache.set_dishes(dishes_schemas)
            return dishes_schemas


    async def creat_dish(self, body: DishCreateSchema, user_id: int) -> DishSchema:
        dish_id = await self.dish_repository.create_dish(body, user_id)
        dish = await self.dish_repository.get_dish_by_index(dish_id)
        return DishSchema.model_validate(dish)


    async def update_dish_name(self, dish_id: int, dish_name: str, user_id: int) -> DishSchema:
        dish = await self.dish_repository.get_user_dish(dish_id=dish_id, user_id=user_id)
        if not dish:
            raise DishNotFound

        dish = await self.dish_repository.update_dish(dish_id=dish_id, new_name=dish_name)
        return DishSchema.model_validate(dish)


    async def delete_dish(self, dish_id: int, user_id: int) -> str:
        dish = await self.dish_repository.get_user_dish(dish_id=dish_id, user_id=user_id)
        if not dish:
                    raise DishNotFound

        await self.dish_repository.delete_dish_by_index(dish_id=dish_id)
        return "Блюдо удалено."
        
