from sqlalchemy.orm import Session, sessionmaker

from models import Dish
from schema import DishSchema
from sqlalchemy import delete, select, update

from typing import Sequence

class DishRepository:

    def __init__(self, db_session: sessionmaker[Session]) -> None:
        self.db_session = db_session

    def get_dish_by_index(self, dish_id) -> Dish | None:
        query = select(Dish).where(Dish.id == dish_id)
        with self.db_session() as session:
            dishes: Dish | None = session.execute(query).scalar_one_or_none()

        return dishes

    def get_all_dishes(self) -> Sequence[Dish]:
        query = select(Dish)
        with self.db_session() as session:
            dishes: Sequence[Dish] = session.execute(query).scalars().all()

        return dishes

    def create_dish(self, new_dish: DishSchema) -> int:
        dish_model = Dish(
                            name=new_dish.name, 
                            calories=new_dish.calories, 
                            price=new_dish.price, 
                            category_id=new_dish.category_id
                        )

        with self.db_session() as session:
            session.add(dish_model)
            session.commit()

            session.refresh(dish_model)
        
        return dish_model.id

    def update_dish(self, dish_id: int, new_name: str) -> Dish:
        query = update(Dish).where(Dish.id == dish_id).values(name = new_name).returning(Dish.id)
        with self.db_session() as session:
            dish_id: int = session.execute(query).scalar_one_or_none()
            session.commit()

        return self.get_dish_by_index(dish_id)

    def delete_dish_by_index(self, dish_id: int) -> dict[str, str]:
        query = delete(Dish).where(Dish.id == dish_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

        return {"message" : "dish was deleted"}

        