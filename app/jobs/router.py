from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.users.model import User
from typing import Optional

from app.jobs.schema import (
    JobCreateSchema,
    JobResponseSchema,
    JobUpdateSchema
)

from app.jobs.service import (
    create_job,
    get_all_jobs,
    get_job,
    search_jobs,
    update_job,
    delete_job
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post(
    "/",
    response_model=JobResponseSchema
)
def create(
    body: JobCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return create_job(
        body,
        db,
        current_user
    )


@router.get(
    "/",
    response_model=list[JobResponseSchema]
)
def get_jobs(
    db: Session = Depends(get_db)
):
    return get_all_jobs(db)


@router.get("/search")
def search(
    search: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(
        get_db
    )
):
    return search_jobs(
        search,
        location,
        db
    )


@router.get(
    "/{job_id}",
    response_model=JobResponseSchema
)
def get_single_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    return get_job(job_id, db)


@router.patch(
    "/{job_id}",
    response_model=JobResponseSchema
)
def update(
    job_id: int,
    body: JobUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return update_job(
        job_id,
        body,
        db,
        current_user
    )


@router.delete("/{job_id}")
def delete(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return delete_job(
        job_id,
        db,
        current_user
    )