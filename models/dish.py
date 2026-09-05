from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Dish(Base):
    __tablename__ = "Dish"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    calories: Mapped[int]
    price: Mapped[int]
    category_id: Mapped[int]

class Category(Base):
    __tablename__ = "Category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
