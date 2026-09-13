from typing import Literal

from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Literal["candidate", "recruiter"]

class UserResponseSchema(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class UserUpdateSchema(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None