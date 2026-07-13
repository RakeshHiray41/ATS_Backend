from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.users.model import User
from app.interviews.schema import (
    InterviewCreateSchema,
    InterviewUpdateSchema,
    InterviewResponseSchema,
    InterviewWithDetailsSchema
)

from app.interviews.service import (
    schedule_interview,
    get_job_interviews,
    get_recruiter_interviews,
    get_my_interviews,
    update_interview,
    delete_interview
)

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"]
)


@router.post(
    "/",
    response_model=InterviewResponseSchema
)
async def create(
    body: InterviewCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return await schedule_interview(
        body,
        db,
        current_user
    )


@router.get(
    "/job/{job_id}",
    response_model=list[InterviewWithDetailsSchema]
)
def list_for_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_job_interviews(
        job_id,
        db,
        current_user
    )


@router.get(
    "/recruiter",
    response_model=list[InterviewWithDetailsSchema]
)
def all_recruiter_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_recruiter_interviews(
        db,
        current_user
    )


@router.get(
    "/my",
    response_model=list[InterviewWithDetailsSchema]
)
def my_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_my_interviews(
        db,
        current_user
    )


@router.patch(
    "/{interview_id}",
    response_model=InterviewResponseSchema
)
def update(
    interview_id: int,
    body: InterviewUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return update_interview(
        interview_id,
        body,
        db,
        current_user
    )


@router.delete("/{interview_id}")
def delete(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return delete_interview(
        interview_id,
        db,
        current_user
    )