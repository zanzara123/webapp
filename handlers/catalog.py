from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from database import Dish
from schema.models import DishSchema
from repository import DishRepository, CacheDishRepository
from service import DishService
from dependecy import get_dish_service


router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/all", response_model=list[DishSchema])
async def get_all_dishes(dish_service: Annotated[DishService, Depends(get_dish_service)]):
    return dish_service.get_all_dishes()


#post
#patch
#delete