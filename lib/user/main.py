# Description: Main file for the User service. This file contains the FastAPI app setup and the endpoints to manage users.
#
# The User service is a simple service that allows users to register and delete their accounts. The service uses an SQLite database to store user data.
#
# The service has the following endpoints:
# - GET /users: Get all users
# - POST /users: Register a new user
# - DELETE /users/{user_id}: Delete a user by ID
#
# The service also includes a dependency to get the database connection and a function to register the service with the Service Catalog.
#
# The service runs on port 8001 and registers itself with the Service Catalog when started.
#
# To run the service, use the following command:
# uvicorn lib.user.main:app --reload
#

from fastapi import FastAPI, HTTPException, Depends
from lib.user.models import UserCreate, UserResponse
from typing import List
import sqlite3
import requests

from config.config import (
    DATABASE_PATH,
    SERVICE_CATALOG_HOST,
    SERVICE_CATALOG_PORT,
    USER_SERVICE_HOST,
    USER_SERVICE_PORT,
)

app = FastAPI()


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()


@app.get("/users", response_model=List[UserResponse])
def get_users(db: sqlite3.Connection = Depends(get_db)) -> List[UserResponse]:
    cursor = db.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    return [UserResponse(id=row[0], username=row[1], email=row[2]) for row in users]


@app.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate, db: sqlite3.Connection = Depends(get_db)
) -> UserResponse:
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (user.username, user.email),
        )
        db.commit()
        user_id = cursor.lastrowid
        return UserResponse(id=user_id, username=user.username, email=user.email)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )


@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: sqlite3.Connection = Depends(get_db)) -> UserResponse:
    cursor = db.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    return UserResponse(id=user[0], username=user[1], email=user[2])


def register_service():
    service_catalog_url = (
        f"http://{SERVICE_CATALOG_HOST}:{SERVICE_CATALOG_PORT}/services"
    )
    service_data = {
        "id": 5,  # Unique ID for the User service
        "name": "User Service",
        "description": "Service for managing users",
    }
    try:
        response = requests.post(service_catalog_url, json=service_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error registering service: {e}")


if __name__ == "__main__":
    import uvicorn

    register_service()
    uvicorn.run(app, host=USER_SERVICE_HOST, port=USER_SERVICE_PORT)
