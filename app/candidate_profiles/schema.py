from typing import List, Optional

from pydantic import BaseModel, field_validator


def _parse_skills(value):
    """Normalize whatever is stored/sent for skills into a clean list[str]."""
    if value is None:
        return None

    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]

    if isinstance(value, str):
        text = value.strip()
        # Handle Postgres array literal style: "{java,python}"
        if text.startswith("{") and text.endswith("}"):
            text = text[1:-1]
        if not text:
            return []
        return [s.strip().strip('"') for s in text.split(",") if s.strip()]

    return value


class CandidateProfileCreateSchema(BaseModel):
    phone: str | None = None
    bio: str | None = None
    skills: Optional[List[str]] = None
    experience: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None

    @field_validator("skills", mode="before")
    @classmethod
    def validate_skills(cls, value):
        return _parse_skills(value)


class CandidateProfileResponseSchema(BaseModel):
    id: int
    phone: str | None
    bio: str | None
    skills: Optional[List[str]] = None
    experience: str | None
    linkedin_url: str | None
    github_url: str | None
    resume_url: str | None
    photo_url: str | None

    @field_validator("skills", mode="before")
    @classmethod
    def validate_skills(cls, value):
        return _parse_skills(value)

    model_config = {
        "from_attributes": True
    }


class CandidateProfileUpdateSchema(BaseModel):
    phone: str | None = None
    bio: str | None = None
    skills: Optional[List[str]] = None
    experience: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None

    @field_validator("skills", mode="before")
    @classmethod
    def validate_skills(cls, value):
        return _parse_skills(value)