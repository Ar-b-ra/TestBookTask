from fastapi import FastAPI, HTTPException, status
from fastapi.params import Query

from schemas.book import Book, BookCreate
from worker.book_worker import BookWorker

app = FastAPI()

book_worker = BookWorker()


# Эндпоинт для добавления новой книги
@app.post(
    "/books/",
    response_model=BookCreate,
    status_code=status.HTTP_201_CREATED,
    description="Create new book",
)
async def create_book(book: Book):
    new_id, book = book_worker.create_book(book)
    return {"id": new_id, "book": book}


# Эндпоинт для получения списка всех книг
@app.get("/books/", response_model=list[Book], description="Get all books")
async def get_books(
    genre: str | None = Query(None, description="Filter books by genre"),
    author: str | None = Query(None, description="Filter books by author"),
):
    return book_worker.get_all_books(genre, author)


@app.get(
    "/books/{book_id}",
    response_model=Book,
    responses={
        404: {"description": "Book not found"},
    },
    description="Get book by id",
)
async def get_book(book_id: int):
    book = book_worker.get_book(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@app.put(
    "/books/{book_id}",
    response_model=Book,
    responses={
        404: {"description": "Book not found"},
    },
    description="Update book by id",
)
async def update_book(book_id: int, updated_book: Book):
    result = book_worker.update_book(book_id=book_id, book_to_update=updated_book)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return result


@app.delete(
    "/books/{book_id}",
    response_model=Book,
    responses={
        404: {"description": "Book not found"},
    },
    description="Delete book by id",
)
async def delete_book(book_id: int):
    result = book_worker.delete_book(book_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return result
