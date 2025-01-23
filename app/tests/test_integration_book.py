from fastapi import status
from fastapi.testclient import TestClient
import pytest
from app import app

BASE_URL = "/books/"


@pytest.fixture
def client():
    # Возвращаем новый экземпляр TestClient для каждого теста
    from app import book_worker

    book_worker._books.clear()
    return TestClient(app)


def test_create_book(client):
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian",
    }
    response = client.post(BASE_URL, json=book_data)
    response_json = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_json["id"] == 0
    assert response_json["book"] == book_data


def test_get_books(client):
    response = client.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_get_books_with_filter(client):
    client
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
        client.post(BASE_URL, json=book)

    test_data = [
        ({"genre": "Dystopian"}, ["1984", "Brave New World"]),
        ({"author": "George Orwell"}, ["1984", "Animal Farm"]),
        ({"genre": "Dystopian", "author": "George Orwell"}, ["1984"]),
        ({}, ["1984", "Animal Farm", "Brave New World", "The Great Gatsby"]),
    ]

    for filter_params, expected_titles in test_data:
        response = client.get(BASE_URL, params=filter_params)

        assert response.status_code == status.HTTP_200_OK

        assert isinstance(response.json(), list)
        returned_titles = [book["title"] for book in response.json()]
        assert returned_titles == expected_titles


def test_get_book_by_id(client):
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian",
    }
    create_response = client.post(BASE_URL, json=book_data)
    create_response_json = create_response.json()
    new_book_id = create_response_json["id"]
    new_book = create_response_json["book"]

    response = client.get(f"{BASE_URL}{new_book_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == new_book


def test_update_book(client):
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian",
    }
    create_response = client.post(BASE_URL, json=book_data)
    book_id = create_response.json()["id"]

    updated_data = {
        "title": "Animal Farm",
        "author": "George Orwell",
        "year": 1945,
        "genre": "Satire",
    }
    response = client.put(f"{BASE_URL}{book_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Animal Farm"
    assert response.json()["genre"] == "Satire"


def test_delete_book(client):
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian",
    }
    create_response = client.post(BASE_URL, json=book_data)
    book_id = create_response.json()["id"]

    response = client.delete(f"{BASE_URL}{book_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == book_data

    get_response = client.get(f"{BASE_URL}{book_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
