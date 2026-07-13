from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.users.model import User

from app.applications.schema import (
    ApplicationResponseSchema,
    ApplicationWithCandidateSchema,
    ApplicationWithJobSchema,
    UpdateApplicationStatusSchema
)

from app.applications.service import (
    apply_job,
    get_job_applications,
    update_application_status,
    get_my_applications
)


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post(
    "/apply/{job_id}",
    response_model=ApplicationResponseSchema
)
def apply(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return apply_job(
        job_id,
        db,
        current_user
    )


@router.get(
    "/job/{job_id}",
    response_model=list[ApplicationWithCandidateSchema]
)
def get_applications(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_job_applications(
        job_id,
        db,
        current_user
    )


@router.patch(
    "/{application_id}/status",
    response_model=ApplicationResponseSchema
)
def update_status(
    application_id: int,
    body: UpdateApplicationStatusSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return update_application_status(
        application_id,
        body,
        db,
        current_user
    )


@router.get(
    "/my",
    response_model=list[
        ApplicationWithJobSchema
    ]
)
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_my_applications(
        db,
        current_user
    )