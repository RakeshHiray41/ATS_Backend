from pydantic import BaseModel
from typing import Optional


class JobCreateSchema(BaseModel):
    title: str
    description: str
    location: str
    experience: str
    salary: str
    company_id: int


class JobUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    experience: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[str] = None


class JobResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    location: str
    experience: str
    salary: str
    status: str
    company_id: int

    model_config = {
        "from_attributes": True
    }