from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: Decimal = Field(default=0)
    stock: int = Field(default=0)
    image_url: str = "/static/products/default.jpg"
    category: str = "Thuốc"
