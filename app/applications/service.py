from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.jobs.model import Job
from app.users.model import User
from app.applications.model import Application
from app.candidate_profiles.model import CandidateProfile


def apply_job(
    job_id: int,
    db: Session,
    current_user: User
):
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=403,
            detail="Candidate only"
        )

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

    profile = (
        db.query(CandidateProfile)
        .filter(
            CandidateProfile.user_id
            == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=400,
            detail="Create profile first"
        )

    if not profile.resume_url:
        raise HTTPException(
            status_code=400,
            detail="Upload resume first"
        )

    already_applied = (
        db.query(Application)
        .filter(
            Application.job_id == job_id,
            Application.candidate_id
            == current_user.id
        )
        .first()
    )

    if already_applied:
        raise HTTPException(
            status_code=400,
            detail="Already applied"
        )

    application = Application(
        job_id=job.id,
        candidate_id=current_user.id,
        resume_url=profile.resume_url
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_job_applications(
    job_id: int,
    db: Session,
    current_user: User
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Recruiter only"
        )

    # Application ला User table shi join karून candidate cha
    # naav ani email fetch kartoy, nahi tar frontend la fakt
    # candidate_id (number) milतो ani "Candidate #3" dakhavावं लागतं.
    rows = (
        db.query(Application, User)
        .join(User, Application.candidate_id == User.id)
        .filter(Application.job_id == job_id)
        .all()
    )

    result = []
    for application, user in rows:
        result.append({
            "id": application.id,
            "status": application.status,
            "applied_at": application.applied_at,
            "job_id": application.job_id,
            "candidate_id": application.candidate_id,
            "resume_url": application.resume_url,
            "candidate_name": user.full_name,
            "candidate_email": user.email,
        })

    return result


def update_application_status(
    application_id: int,
    body,
    db: Session,
    current_user
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Recruiter only"
        )

    application = (
        db.query(Application)
        .filter(
            Application.id
            == application_id
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    application.status = body.status

    db.commit()
    db.refresh(application)

    return application


def get_my_applications(
    db: Session,
    current_user
):
    rows = (
        db.query(Application, Job)
        .join(Job, Application.job_id == Job.id)
        .filter(Application.candidate_id == current_user.id)
        .all()
    )

    result = []
    for application, job in rows:
        result.append({
            "id": application.id,
            "status": application.status,
            "applied_at": application.applied_at,
            "job_id": application.job_id,
            "candidate_id": application.candidate_id,
            "resume_url": application.resume_url,
            "job_title": job.title,
        })

    return result