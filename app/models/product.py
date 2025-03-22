from typing import Optional
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    title: str
    price: float
    rating: Optional[float]
    url: str
    brand: Optional[str]
    img: Optional[str]
    scrape_timestamp: str