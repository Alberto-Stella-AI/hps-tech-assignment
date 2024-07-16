from fastapi.testclient import TestClient
from lib.user.main import app, get_db, register_service
import sqlite3
from unittest.mock import patch
from config.config import SERVICE_CATALOG_HOST, SERVICE_CATALOG_PORT

client = TestClient(app)


def override_get_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT UNIQUE
        )
    """
    )
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        ("testuser", "testuser@example.com"),
    )
    conn.commit()
    try:
        yield conn
    finally:
        conn.close()


app.dependency_overrides[get_db] = override_get_db


# Test retrieving all users
def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == "testuser"


# Test creating a new user
def test_create_user():
    new_user = {"username": "newuser", "email": "newuser@example.com"}
    response = client.post("/users", json=new_user)
    assert response.status_code == 200
    assert response.json()["username"] == new_user["username"]


# Test creating a user with an existing username
def test_create_user_existing_username():
    existing_user = {"username": "testuser", "email": "duplicate@example.com"}
    response = client.post("/users", json=existing_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"


# Test deleting a non-existing user
def test_delete_non_existing_user():
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# Test service registration
@patch("lib.user.main.requests.post")
def test_register_service(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "registered"}

    register_service()
    mock_post.assert_called_once_with(
        f"http://{SERVICE_CATALOG_HOST}:{SERVICE_CATALOG_PORT}/services",
        json={
            "id": 5,
            "name": "User Service",
            "description": "Service for managing users",
        },
    )
