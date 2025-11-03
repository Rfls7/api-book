from typing import Optional, List
from pydantic import BaseModel


class Book(BaseModel):
    id: str
    title: str
    price: float
    stock: int
    rating: int
    category: Optional[str]
    product_page_url: str
    upc: Optional[str]
    description: Optional[str]
    image_url: Optional[str]


class BookList(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Book]
