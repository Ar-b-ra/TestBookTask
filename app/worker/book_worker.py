from schemas.book import Book


class BookWorker:
    def __init__(self):
        self._books = {}

    def get_book(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def get_all_books(self) -> list[Book]:
        return [value for value in self._books.values()]

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

    def delete_book(self, book_id: int) -> Book | None:
        return self._books.pop(book_id, default=None)
