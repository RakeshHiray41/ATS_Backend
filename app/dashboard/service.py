from sqlalchemy.orm import Session
from app.jobs.model import Job
from app.applications.model import Application
from app.interviews.model import Interview
from app.candidate_profiles.model import CandidateProfile
from app.companies.model import Company


def recruiter_dashboard(
    db: Session,
    current_user
):
    # Scope everything to jobs owned by THIS recruiter's company — the
    # previous version counted every job/application/interview in the
    # whole system, which leaked other recruiters' numbers onto this
    # recruiter's dashboard.
    company = (
        db.query(Company)
        .filter(Company.owner_id == current_user.id)
        .first()
    )

    if not company:
        return {
            "total_jobs": 0,
            "total_applications": 0,
            "applicants": 0,
            "shortlisted": 0,
            "interviews": 0,
            "company": None
        }

    total_jobs = (
        db.query(Job)
        .filter(Job.company_id == company.id)
        .count()
    )

    total_applications = (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .filter(Job.company_id == company.id)
        .count()
    )

    shortlisted = (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .filter(
            Job.company_id == company.id,
            Application.status == "shortlisted"
        )
        .count()
    )

    interviews = (
        db.query(Interview)
        .join(Application, Interview.application_id == Application.id)
        .join(Job, Application.job_id == Job.id)
        .filter(Job.company_id == company.id)
        .count()
    )

    return {
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        # "applicants" is what the frontend dashboard card actually reads —
        # keeping both keys so nothing else that relies on
        # total_applications breaks.
        "applicants": total_applications,
        "shortlisted": shortlisted,
        "interviews": interviews,
        "company": company.name
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