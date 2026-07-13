from pydantic import BaseModel


class CompanyCreateSchema(BaseModel):
    name: str
    description: str
    website: str
    location: str


class CompanyResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    website: str
    location: str
    logo_url: str | None

    model_config = {
        "from_attributes": True
    }

class CompanyUpdateSchema(
    BaseModel
):
    name: str | None = None
    description: str | None = None
    website: str | None = None
    location: str | None = None