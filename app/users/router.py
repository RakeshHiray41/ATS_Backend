from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.users.schema import UserRegisterSchema , UserResponseSchema
from app.users.service import register_user , login_user , become_recruiter ,delete_user ,update_user
from app.users.schema import  UserLoginSchema, TokenSchema ,UserUpdateSchema
from app.core.dependencies import get_current_user
from app.users.model import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register" , response_model=UserResponseSchema)
def register(
    body: UserRegisterSchema,
    db: Session = Depends(get_db)
):
    return register_user(body, db)

@router.post(
    "/login",
    response_model=TokenSchema
)
def login(
    body: UserLoginSchema,
    db: Session = Depends(get_db)
):
    return login_user(body, db)

@router.get("/me" , response_model=UserResponseSchema)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.patch("/become-recruiter" ,response_model=UserResponseSchema)
def upgrade_role(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return become_recruiter(
        current_user,
        db
    )

@router.patch(
    "/me",
    response_model=UserResponseSchema
)
def update(
    body: UserUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return update_user(
        body,
        db,
        current_user
    )


@router.delete("/me")
def delete(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return delete_user(
        db,
        current_user
    )