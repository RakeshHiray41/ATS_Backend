from sqlalchemy.orm import Session
from app.jobs.model import Job
from app.applications.model import Application
from app.interviews.model import Interview
from app.candidate_profiles.model import CandidateProfile


def recruiter_dashboard(
    db: Session,
    current_user
):
    total_jobs = (
        db.query(Job)
        .count()
    )

    total_applications = (
        db.query(Application)
        .count()
    )

    shortlisted = (
        db.query(Application)
        .filter(
            Application.status
            == "Shortlisted"
        )
        .count()
    )

    interviews = (
        db.query(Interview)
        .count()
    )

    return {
        "total_jobs": total_jobs,
        "total_applications":
            total_applications,
        "shortlisted":
            shortlisted,
        "interviews":
            interviews
    }


def candidate_dashboard(
    db: Session,
    current_user
):
    applied_jobs = (
        db.query(Application)
        .filter(
            Application.candidate_id
            == current_user.id
        )
        .count()
    )

    upcoming_interviews = (
        db.query(Interview)
        .join(
            Application,
            Interview.application_id
            == Application.id
        )
        .filter(
            Application.candidate_id
            == current_user.id
        )
        .count()
    )

    profile = (
        db.query(
            CandidateProfile
        )
        .filter(
            CandidateProfile.user_id
            == current_user.id
        )
        .first()
    )

    completion = 0

    if profile:
        if profile.phone:
            completion += 20
        if profile.skills:
            completion += 20
        if profile.resume_url:
            completion += 20
        if profile.photo_url:
            completion += 20
        if profile.linkedin_url:
            completion += 20

    return {
        "applied_jobs":
            applied_jobs,
        "upcoming_interviews":
            upcoming_interviews,
        "profile_completion":
            completion
    }