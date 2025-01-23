import pytest
from schemas.book import Book
from worker.book_worker import BookWorker


@pytest.fixture
def book_worker():
    return BookWorker()


@pytest.fixture
def sample_book():
    return Book(title="Sample Book", author="John Doe", genre="Fiction", year="2025")


def test_create_book(book_worker, sample_book):
    book_id, created_book = book_worker.create_book(sample_book)
    assert book_id == 0
    assert created_book.title == "Sample Book"
    assert created_book.author == "John Doe"
    assert created_book.genre == "Fiction"


def test_get_book(book_worker, sample_book):
    book_id, _ = book_worker.create_book(sample_book)
    retrieved_book = book_worker.get_book(book_id)
    assert retrieved_book is not None
    assert retrieved_book.title == "Sample Book"
    assert retrieved_book.author == "John Doe"
    assert retrieved_book.genre == "Fiction"


def test_get_all_books(book_worker, sample_book):
    book_worker.create_book(sample_book)
    books = book_worker.get_all_books(genre=None, author=None)
    assert len(books) == 1
    assert books[0].title == "Sample Book"


@pytest.mark.parametrize(
    "filter_params, expected_titles",
    [
        ({"genre": "Dystopian"}, ["1984", "Brave New World"]),
        ({"author": "George Orwell"}, ["1984", "Animal Farm"]),
        ({"genre": "Dystopian", "author": "George Orwell"}, ["1984"]),
        ({}, ["1984", "Animal Farm", "Brave New World", "The Great Gatsby"]),
    ],
)
def test_get_books_with_filter(book_worker, filter_params, expected_titles):
    test_books = [
        {
            "title": "1984",
            "author": "George Orwell",
            "year": 1949,
            "genre": "Dystopian",
        },
        {
            "title": "Animal Farm",
            "author": "George Orwell",
            "year": 1945,
            "genre": "Satire",
        },
        {
            "title": "Brave New World",
            "author": "Aldous Huxley",
            "year": 1932,
            "genre": "Dystopian",
        },
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "year": 1925,
            "genre": "Fiction",
        },
    ]
    for book in test_books:
        book_worker.create_book(Book(**book))
    books = book_worker.get_all_books(**filter_params)
    returned_titles = [book.title for book in books]
    assert returned_titles == expected_titles


def test_get_all_books_by_author(book_worker, sample_book):
    book_worker.create_book(sample_book)
    books = book_worker.get_all_books(genre=None, author="John Doe")
    assert len(books) == 1
    assert books[0].author == "John Doe"


@pytest.mark.parametrize(
    "book_id,updated_book",
    [
        (
            0,
            Book(
                title="Updated Book", author="Jane Doe", genre="Non-Fiction", year=2010
            ),
        ),
        (-1, None),
    ],
)
def test_update_book(book_id, updated_book, book_worker, sample_book):
    book_worker.create_book(sample_book)
    update_result = book_worker.update_book(
        book_id,
        Book(title="Updated Book", author="Jane Doe", genre="Non-Fiction", year=2010),
    )
    assert update_result == updated_book


def test_delete_book(book_worker, sample_book):
    book_id, _ = book_worker.create_book(sample_book)
    deleted_book = book_worker.delete_book(book_id)
    assert deleted_book is not None
    assert deleted_book.title == "Sample Book"
    assert book_worker.get_book(book_id) is None


def test_delete_nonexistent_book(book_worker):
    deleted_book = book_worker.delete_book(999)
    assert deleted_book is None
