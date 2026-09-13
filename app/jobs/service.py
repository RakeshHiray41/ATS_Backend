from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.jobs.model import Job
from app.companies.model import Company
from app.applications.model import Application
from app.interviews.model import Interview
from sqlalchemy import or_


def create_job(
    body,
    db: Session,
    current_user
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Recruiter only"
        )

    company = (
        db.query(Company)
        .filter(
            Company.id == body.company_id
        )
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    if company.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't own this company"
        )

    job = Job(
        title=body.title,
        description=body.description,
        location=body.location,
        experience=body.experience,
        salary=body.salary,
        company_id=body.company_id,
        status="open"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_all_jobs(
    db: Session,
    current_user
):
    if current_user.role == "recruiter":
        company = (
            db.query(Company)
            .filter(Company.owner_id == current_user.id)
            .first()
        )

        if not company:
            return []

        return (
            db.query(Job)
            .filter(Job.company_id == company.id)
            .all()
        )

    return db.query(Job).all()


def get_job(job_id: int, db: Session):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


def search_jobs(
    search: str,
    location: str,
    db: Session
):
    query = db.query(Job)

    if search:
        query = query.filter(
            Job.title.ilike(
                f"%{search}%"
            )
        )

    if location:
        query = query.filter(
            Job.location.ilike(
                f"%{location}%"
            )
        )

    return query.all()


def update_job(
    job_id: int,
    body,
    db: Session,
    current_user
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    company = (
        db.query(Company)
        .filter(Company.id == job.company_id)
        .first()
    )

    if not company or company.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to edit this job"
        )

    data = body.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)

    return job


def delete_job(
    job_id: int,
    db: Session,
    current_user
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    company = (
        db.query(Company)
        .filter(Company.id == job.company_id)
        .first()
    )

    if not company or company.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this job"
        )

    # Job delete karnyaadhi, chain follow karava lagto:
    # Interview -> Application -> Job (FK constraints mule)

    application_ids = [
        row.id
        for row in db.query(Application.id)
        .filter(Application.job_id == job_id)
        .all()
    ]

    if application_ids:
        db.query(Interview).filter(
            Interview.application_id.in_(application_ids)
        ).delete(synchronize_session=False)

    db.query(Application).filter(Application.job_id == job_id).delete()

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted"
    }