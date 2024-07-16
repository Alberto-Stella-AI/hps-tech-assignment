"""Module for dynamic configuration variables of the project."""
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
DATABASE_PATH = ROOT_PATH.joinpath("db", "users.db")
DATA_PATH = ROOT_PATH.joinpath
SERVICE_CATALOG_HOST = "0.0.0.0"
SERVICE_CATALOG_PORT = 8000
USER_SERVICE_HOST = "0.0.0.0"
USER_SERVICE_PORT = 8001
