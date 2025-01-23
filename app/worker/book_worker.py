from worker.base import BookWorkerBase
from schemas.book import Book


class BookWorker(BookWorkerBase):
    def __init__(self):
        self._books = {}

    def get_book(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def get_all_books(self, genre: str | None, author: str | None) -> list[Book]:
        filtered_books = []
        genre_lower = genre.lower() if genre else None
        author_lower = author.lower() if author else None

        for book in self._books.values():
            if genre_lower is not None and book.genre.lower() != genre_lower:
                continue
            if author_lower is not None and book.author.lower() != author_lower:
                continue
            filtered_books.append(book)

        return filtered_books

    def create_book(self, new_book: Book) -> tuple[int, Book]:
        i = 0
        while i in self._books.keys():
            i += 1
        self._books[i] = new_book
        return i, new_book

    def update_book(self, book_id, book_to_update: Book) -> Book | None:
        if book_id not in self._books:
            return
        self._books[book_id] = book_to_update
        return book_to_update

    def delete_book(self, book_id: int) -> Book | None:
        return self._books.pop(book_id, None)
