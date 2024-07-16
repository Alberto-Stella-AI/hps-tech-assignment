import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from lib.service_catalog.models import Service
from lib.service_catalog.main import app, services_db

# Sample data for tests
sample_services = [
    Service(id=1, name="Service 1", description="Description for Service 1"),
    Service(id=2, name="Service 2", description="Description for Service 2"),
    Service(id=3, name="Service 3", description="Description for Service 3"),
    Service(id=4, name="Service 4", description="Description for Service 4"),
]


@pytest.fixture
def test_app() -> FastAPI:
    return app


@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Setup
    services_db.clear()
    services_db.extend(sample_services)
    yield
    # Teardown
    services_db.clear()


@pytest.mark.asyncio
async def test_get_services(client: TestClient):
    response = client.get("/services")
    assert response.status_code == 200
    assert len(response.json()) == 4
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_service(client: TestClient):
    response = client.get("/services/1")
    assert response.status_code == 200
    service = response.json()
    assert service["id"] == 1
    assert service["name"] == "Service 1"


@pytest.mark.asyncio
async def test_get_service_not_found(client: TestClient):
    response = client.get("/services/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Service not found"}


@pytest.mark.asyncio
async def test_create_service(client: TestClient):
    new_service = {
        "id": 5,
        "name": "Service 5",
        "description": "Description for Service 5",
    }
    response = client.post("/services", json=new_service)
    assert response.status_code == 200
    service = response.json()
    assert service["id"] == 5
    assert service["name"] == "Service 5"


@pytest.mark.asyncio
async def test_create_service_existing_id(client: TestClient):
    new_service = {
        "id": 1,
        "name": "Service 5",
        "description": "Description for Service 5",
    }
    response = client.post("/services", json=new_service)
    assert response.status_code == 400
    assert response.json() == {"detail": "Service ID already exists"}


@pytest.mark.asyncio
async def test_update_service(client: TestClient):
    updated_service = {
        "id": 1,
        "name": "Updated Service 1",
        "description": "Updated description",
    }
    response = client.put("/services/1", json=updated_service)
    assert response.status_code == 200
    service = response.json()
    assert service["name"] == "Updated Service 1"


@pytest.mark.asyncio
async def test_update_service_not_found(client: TestClient):
    updated_service = {
        "id": 999,
        "name": "Updated Service",
        "description": "Updated description",
    }
    response = client.put("/services/999", json=updated_service)
    assert response.status_code == 404
    assert response.json() == {"detail": "Service not found"}


@pytest.mark.asyncio
async def test_delete_service(client: TestClient):
    response = client.delete("/services/1")
    assert response.status_code == 200
    service = response.json()
    assert service["id"] == 1


@pytest.mark.asyncio
async def test_delete_service_not_found(client: TestClient):
    response = client.delete("/services/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Service not found"}
