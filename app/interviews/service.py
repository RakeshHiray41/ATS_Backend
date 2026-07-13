from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.interviews.model import Interview
from app.applications.model import Application
from app.jobs.model import Job
from app.companies.model import Company
from app.users.model import User
from app.mail.service import send_email


async def schedule_interview(
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
            == body.application_id
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    interview = Interview(
        application_id=body.application_id,
        interview_date=body.interview_date,
        meeting_link=body.meeting_link,
        notes=body.notes
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    candidate = (
        db.query(User)
        .filter(
            User.id
            == application.candidate_id
        )
        .first()
    )

    job = (
        db.query(Job)
        .filter(Job.id == application.job_id)
        .first()
    )

    company = (
        db.query(Company)
        .filter(Company.id == job.company_id)
        .first()
    ) if job else None

    formatted_date = interview.interview_date.strftime("%A, %d %B %Y at %I:%M %p")

    email_body = f"""
    <div style="font-family: Arial, Helvetica, sans-serif; max-width: 560px; margin: 0 auto; color: #1e293b;">
      <div style="background-color: #4f46e5; padding: 24px; border-radius: 10px 10px 0 0;">
        <h1 style="color: #ffffff; margin: 0; font-size: 20px;">Interview Scheduled</h1>
      </div>
      <div style="border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 10px 10px; padding: 24px;">
        <p style="font-size: 15px;">Hello {candidate.full_name},</p>
        <p style="font-size: 15px; line-height: 1.6;">
          Good news! <strong>{company.name if company else "The hiring team"}</strong> has scheduled
          an interview with you for the <strong>{job.title if job else "position"}</strong> role.
        </p>

        <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;">
          <tr>
            <td style="padding: 8px 0; color: #64748b;">Company</td>
            <td style="padding: 8px 0; font-weight: 600;">{company.name if company else "-"}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #64748b;">Position</td>
            <td style="padding: 8px 0; font-weight: 600;">{job.title if job else "-"}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #64748b;">Date &amp; Time</td>
            <td style="padding: 8px 0; font-weight: 600;">{formatted_date}</td>
          </tr>
        </table>

        <a href="{interview.meeting_link}"
           style="display: inline-block; background-color: #4f46e5; color: #ffffff; text-decoration: none;
                  padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 14px;">
          Join Meeting
        </a>

        {f'<p style="margin-top: 20px; font-size: 14px; color: #475569;"><strong>Notes:</strong> {interview.notes}</p>' if interview.notes else ""}

        <p style="margin-top: 24px; font-size: 13px; color: #94a3b8;">
          If you have any questions, please reach out to the recruiter directly.
        </p>
      </div>
    </div>
    """

    await send_email(
        subject=f"Interview Scheduled - {job.title if job else 'Your Application'}",
        email=candidate.email,
        body=email_body
    )

    return interview


def _row_to_details_dict(interview, application, job, user, company):
    return {
        "id": interview.id,
        "application_id": interview.application_id,
        "interview_date": interview.interview_date,
        "meeting_link": interview.meeting_link,
        "status": interview.status,
        "notes": interview.notes,
        "candidate_name": user.full_name,
        "candidate_email": user.email,
        "job_title": job.title,
        "company_name": company.name,
    }


def get_job_interviews(
    job_id: int,
    db: Session,
    current_user
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Recruiter only"
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

    company = (
        db.query(Company)
        .filter(Company.id == job.company_id)
        .first()
    )

    if not company or company.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view interviews for this job"
        )

    rows = (
        db.query(Interview, Application, User)
        .join(Application, Interview.application_id == Application.id)
        .join(User, Application.candidate_id == User.id)
        .filter(Application.job_id == job_id)
        .all()
    )

    return [
        _row_to_details_dict(interview, application, job, user, company)
        for interview, application, user in rows
    ]


def get_recruiter_interviews(
    db: Session,
    current_user
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Recruiter only"
        )

    rows = (
        db.query(Interview, Application, Job, User, Company)
        .join(Application, Interview.application_id == Application.id)
        .join(Job, Application.job_id == Job.id)
        .join(Company, Job.company_id == Company.id)
        .join(User, Application.candidate_id == User.id)
        .filter(Company.owner_id == current_user.id)
        .all()
    )

    return [
        _row_to_details_dict(interview, application, job, user, company)
        for interview, application, job, user, company in rows
    ]


def get_my_interviews(
    db: Session,
    current_user
):
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=403,
            detail="Candidate only"
        )

    rows = (
        db.query(Interview, Application, Job, Company)
        .join(Application, Interview.application_id == Application.id)
        .join(Job, Application.job_id == Job.id)
        .join(Company, Job.company_id == Company.id)
        .filter(Application.candidate_id == current_user.id)
        .all()
    )

    return [
        _row_to_details_dict(interview, application, job, current_user, company)
        for interview, application, job, company in rows
    ]


def _get_owned_interview(interview_id: int, db: Session, current_user):
    interview = (
        db.query(Interview)
        .filter(Interview.id == interview_id)
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    application = (
        db.query(Application)
        .filter(Application.id == interview.application_id)
        .first()
    )

    job = (
        db.query(Job)
        .filter(Job.id == application.job_id)
        .first()
    )

    company = (
        db.query(Company)
        .filter(Company.id == job.company_id)
        .first()
    )

    if not company or company.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to modify this interview"
        )

    return interview


def update_interview(
    interview_id: int,
    body,
    db: Session,
    current_user
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Recruiter only"
        )

    interview = _get_owned_interview(interview_id, db, current_user)

    data = body.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(interview, key, value)

    db.commit()
    db.refresh(interview)

    return interview


def delete_interview(
    interview_id: int,
    db: Session,
    current_user
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Recruiter only"
        )

    interview = _get_owned_interview(interview_id, db, current_user)

    db.delete(interview)
    db.commit()

    return {
        "message": "Interview cancelled"
    }