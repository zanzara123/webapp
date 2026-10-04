import time

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from typing import Annotated
# from models import Dish
from schema.models import DishSchema, DishCreateSchema
from service import DishService
from dependecy import get_dish_service, get_request_user_id
from models import Dish

from exception import DishNotFound


router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/all", response_model=list[DishSchema])
async def get_all_dishes(
    dish_service: Annotated[DishService, Depends(get_dish_service)],
    user_id: int = Depends(get_request_user_id)
):
    return await dish_service.get_all_dishes()


@router.post('/')
async def create_dish(
    body: DishCreateSchema,
    dish_service: Annotated[DishService, Depends(get_dish_service)],
    user_id: int = Depends(get_request_user_id)
):
    dish = await dish_service.creat_dish(body, user_id)
    return dish


@router.patch('/{dish_id}')
async def patch_dish(
    dish_id: int,
    dish_name: str,
    dish_service: Annotated[DishService, Depends(get_dish_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        return await dish_service.update_dish_name(dish_id=dish_id, dish_name=dish_name, user_id=user_id)

    except DishNotFound as e:
            raise HTTPException(
                status_code = 404,
                detail = e.detail
            )


@router.delete('/{dish_id}')
async def delete_dish(
    dish_id: int,
    dish_service: Annotated[DishService, Depends(get_dish_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        return await dish_service.delete_dish(dish_id, user_id)

    except DishNotFound as e:
        raise HTTPException(
            status_code = 404,
            detail = e.detail
        )

