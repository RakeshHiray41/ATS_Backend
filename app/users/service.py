from sqlalchemy.orm import Session

from app.users.model import User
from app.users.schema import UserRegisterSchema , UserUpdateSchema
from app.core.security import hash_password

from app.users.schema import (
    UserRegisterSchema,
    UserLoginSchema
)

from fastapi import HTTPException
from app.core.security import (
    verify_password,
    create_access_token
)

def register_user(
    body: UserRegisterSchema,
    db: Session
):
    existing_user = (
        db.query(User)
        .filter(User.email == body.email)
        .first()
    )

    if existing_user:
        raise Exception("Email already exists")

    new_user = User(
        full_name=body.full_name,
        email=body.email,
        password=hash_password(body.password),
        role="candidate"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(
    body: UserLoginSchema,
    db: Session
):
    user = (
        db.query(User)
        .filter(User.email == body.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        body.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def become_recruiter(
    current_user,
    db: Session
):
    current_user.role = "recruiter"

    db.commit()
    db.refresh(current_user)

    return current_user

def update_user(
    body: UserUpdateSchema,
    db: Session,
    current_user: User
):
    if body.full_name:
        current_user.full_name = body.full_name

    if body.email:
        current_user.email = body.email

    if body.password:
        current_user.password = hash_password(
            body.password
        )

    db.commit()
    db.refresh(current_user)

    return current_user

def delete_user(
    db: Session,
    current_user: User
):
    db.delete(current_user)
    db.commit()

    return {
        "message":
        "Account deleted"
    }