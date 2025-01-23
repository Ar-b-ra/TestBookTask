from datetime import datetime
from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str = Field(
        min_length=1, max_length=100, description="The title of the book"
    )
    author: str = Field(
        min_length=1, max_length=100, description="The author of the book"
    )
    year: int = Field(
        ge=1000, le=datetime.now().year, description="The year of publication"
    )
    genre: str | None = Field(min_length=1, max_length=50, description="The genre of the book", default=None)


class BookCreate(BaseModel):
    id: int
    book: Book
