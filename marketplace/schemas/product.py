from typing import List, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    currency: Literal['RUB', 'USD']
    category: str | None = None

    class Config:
        from_attributes = True


class ProductWithTimeSchema(ProductSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class ProductsSchema(BaseModel):
    items: List[ProductWithTimeSchema]
    total: int
    page: int
    per_page: int
    pages: int

    class Config:
        from_attributes = True
