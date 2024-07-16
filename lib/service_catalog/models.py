from pydantic import BaseModel
from typing import Optional


class Service(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
