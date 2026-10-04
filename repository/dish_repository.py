from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from models import Dish
from schema import DishSchema, DishCreateSchema
from sqlalchemy import delete, select, update

from typing import Sequence


class DishRepository:

    def __init__(self, db_session: async_sessionmaker[AsyncSession]) -> None:
        self.db_session = db_session


    async def get_dish_by_index(self, dish_id) -> Dish | None:
        query = select(Dish).where(Dish.id == dish_id)
        async with self.db_session as session:
            dish: Dish | None = (await session.execute(query)).scalar_one_or_none()
        return dish


    async def get_user_dish(self, dish_id: int, user_id: int) -> Dish | None:
        query = select(Dish).where(Dish.id == dish_id, Dish.user_id == user_id)
        async with self.db_session as session:
            dishes: Dish | None = (await session.execute(query)).scalar_one_or_none()
        return dishes


    async def get_all_dishes(self) -> Sequence[Dish]:
        query = select(Dish)
        async with self.db_session as session:
            dishes: Sequence[Dish] = ( await session.execute(query)).scalars().all()
        return dishes


    async def create_dish(self, new_dish: DishCreateSchema, user_id: int) -> int:
        dish_model = Dish(
            name=new_dish.name, 
            calories=new_dish.calories, 
            price=new_dish.price, 
            category_id=new_dish.category_id,
            user_id = user_id
        )
        async with self.db_session as session:
            session.add(dish_model)
            await session.commit()

            await session.refresh(dish_model)
        return dish_model.id


    async def update_dish(self, dish_id: int, new_name: str) -> Dish:
        query = update(Dish).where(Dish.id == dish_id).values(name = new_name).returning(Dish.id)
        async with self.db_session as session:
            dish_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
        return await self.get_dish_by_index(dish_id)


    async def delete_dish_by_index(self, dish_id: int) -> dict[str, str]:
        query = delete(Dish).where(Dish.id == dish_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
        return {"message" : "dish was deleted"}
        