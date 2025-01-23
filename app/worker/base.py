from abc import ABC
from abc import abstractmethod

from schemas.book import Book


class BookWorkerBase(ABC):
    def __init__(self):
        self._books = {}

    @abstractmethod
    def get_book(self, book_id: int) -> Book | None: ...

    @abstractmethod
    def get_all_books(self, genre: str | None, author: str | None) -> list[Book]: ...

    @abstractmethod
    def create_book(self, new_book: Book) -> tuple[int, Book]: ...

    @abstractmethod
    def update_book(self, book_id, book_to_update: Book) -> Book | None: ...

    @abstractmethod
    def delete_book(self, book_id: int) -> Book | None: ...
