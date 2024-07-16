from fastapi import FastAPI, HTTPException
from typing import List
from config.config import SERVICE_CATALOG_HOST, SERVICE_CATALOG_PORT
from lib.service_catalog.models import Service

app = FastAPI()

# In-memory sample database
services_db = [
    Service(id=1, name="Service 1", description="Description for Service 1"),
    Service(id=2, name="Service 2", description="Description for Service 2"),
    Service(id=3, name="Service 3", description="Description for Service 3"),
    Service(id=4, name="Service 4", description="Description for Service 4"),
]


@app.get("/services", response_model=List[Service])
def get_services() -> List[Service]:
    return services_db


@app.get("/services/{service_id}", response_model=Service)
def get_service(service_id: int) -> Service:
    service = next(
        (service for service in services_db if service.id == service_id), None
    )
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@app.post("/services", response_model=Service)
def create_service(service: Service) -> Service:
    if any(svc.id == service.id for svc in services_db):
        raise HTTPException(status_code=400, detail="Service ID already exists")
    services_db.append(service)
    return service


@app.put("/services/{service_id}", response_model=Service)
def update_service(service_id: int, updated_service: Service) -> Service:
    for index, service in enumerate(services_db):
        if service.id == service_id:
            services_db[index] = updated_service
            return updated_service
    raise HTTPException(status_code=404, detail="Service not found")


@app.delete("/services/{service_id}", response_model=Service)
def delete_service(service_id: int) -> Service:
    for index, service in enumerate(services_db):
        if service.id == service_id:
            deleted_service = services_db.pop(index)
            return deleted_service
    raise HTTPException(status_code=404, detail="Service not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=SERVICE_CATALOG_HOST, port=SERVICE_CATALOG_PORT)
