from pydantic import BaseModel, ConfigDict


class DishSchema(BaseModel):
    id: int | None = None
    name: str
    calories: int
    price: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)