from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.users.model import User
from app.companies.schema import CompanyCreateSchema, CompanyResponseSchema, CompanyUpdateSchema
from app.companies.service import (
    create_company,
    delete_company,
    update_company,
    get_my_company,
)
from app.companies.model import Company
from app.core.supabase import supabase


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.post(
    "/",
    response_model=CompanyResponseSchema
)
def create(
    body: CompanyCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_company(
        body,
        db,
        current_user
    )


# NOTE: "/me" MUST come before "/{company_id}" routes,
# otherwise FastAPI will match "me" as company_id and fail.
@router.get(
    "/me",
    response_model=CompanyResponseSchema
)
def me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_company(db, current_user)


@router.patch(
    "/{company_id}"
)
def update(
    company_id: int,
    body: CompanyUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return update_company(
        company_id,
        body,
        db,
        current_user
    )


@router.delete(
    "/{company_id}"
)
def delete(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return delete_company(
        company_id,
        db,
        current_user
    )


@router.post("/{company_id}/upload-logo")
async def upload_logo(
    company_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    company = (
        db.query(Company)
        .filter(
            Company.id == company_id
        )
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    file_extension = (
        file.filename.split(".")[-1]
    )

    file_name = (
        f"{company.id}_"
        f"{uuid.uuid4()}."
        f"{file_extension}"
    )

    file_content = await file.read()

    supabase.storage.from_(
        "company-logos"
    ).upload(
        file_name,
        file_content
    )

    logo_url = (
        supabase.storage
        .from_("company-logos")
        .get_public_url(file_name)
    )

    company.logo_url = logo_url

    db.commit()
    db.refresh(company)

    return {
        "logo_url": logo_url
    }