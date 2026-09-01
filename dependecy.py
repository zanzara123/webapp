from database import get_db_session
from cache import get_redis_connection
from repository import DishRepository, CacheDishRepository
from service import DishService

from fastapi import Depends


def get_dish_repository() -> DishRepository:
    db_session = get_db_session()

    return DishRepository(db_session)


def get_cache_dish_repository() -> CacheDishRepository:
    redis_connection = get_redis_connection()
    return CacheDishRepository(redis_connection)


def get_dish_service(
        dish_repository: DishRepository = Depends(get_dish_repository),
        dish_cache: CacheDishRepository = Depends(get_cache_dish_repository)
    ) -> DishService:
    
    
    return DishService(
        dish_repository = dish_repository, 
        dish_cache=dish_cache
    )