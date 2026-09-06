from fastapi import APIRouter, Depends
from typing import Annotated
# from models import Dish
from schema.models import DishSchema
from service import DishService
from dependecy import get_dish_service, get_request_user_id


router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/all", response_model=list[DishSchema])
async def get_all_dishes(
    dish_service: Annotated[DishService, Depends(get_dish_service)],
    user_id: int = Depends(get_request_user_id)
):
    return dish_service.get_all_dishes()


#post
#patch
#delete