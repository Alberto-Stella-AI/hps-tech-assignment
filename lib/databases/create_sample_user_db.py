# create_users_db.py
import sqlite3
from config.config import DATABASE_PATH
import os


def create_sample_user_database():
    # Ensure the db directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_sample_user_database()
