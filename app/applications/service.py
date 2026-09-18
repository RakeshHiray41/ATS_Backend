from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.jobs.model import Job
from app.users.model import User
from app.applications.model import Application
from app.candidate_profiles.model import CandidateProfile
from app.companies.model import Company
from app.interviews.model import Interview
from app.notifications.service import create_notification

# fastapi-mail is optional: the pre-existing app/mail module was scaffolded
# but never actually wired into the app or added to requirements.txt. We
# import it defensively so a missing package doesn't crash the whole
# server on startup — email alerts just silently no-op if it's absent.
try:
    from app.mail.service import send_email
except ImportError:
    send_email = None


def delete_application(
    application_id: int,
    db: Session,
    current_user: User
):
    """Lets a candidate withdraw their own application."""

    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    if application.candidate_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only withdraw your own applications"
        )

    # Remove any interviews tied to this application first — otherwise the
    # foreign key on interviews.application_id blocks the delete.
    db.query(Interview).filter(
        Interview.application_id == application_id
    ).delete()

    db.delete(application)
    db.commit()

    return {"detail": "Application withdrawn"}


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

    # Make sure this job actually belongs to the current recruiter's
    # company — otherwise any recruiter could view any other recruiter's
    # applicants just by guessing a job_id.
    job = (
        db.query(Job)
        .join(Company, Job.company_id == Company.id)
        .filter(
            Job.id == job_id,
            Company.owner_id == current_user.id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
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


STATUS_MESSAGES = {
    "shortlisted": "You've been shortlisted for {job_title}!",
    "interview_scheduled": "An interview has been scheduled for your application to {job_title}.",
    "hired": "Congratulations! You've been hired for {job_title}.",
    "rejected": "Your application for {job_title} was not selected this time.",
    "applied": "Your application for {job_title} is under review.",
}

# Fuller, more professional copy used specifically in the email — the
# short version in STATUS_MESSAGES is still used for the in-app
# notification, where space is tight.
EMAIL_STATUS_COPY = {
    "shortlisted": (
        "We're pleased to let you know that your application for the "
        "<strong>{job_title}</strong> position has been shortlisted. "
        "Our hiring team was impressed with your profile and will be in "
        "touch shortly with next steps."
    ),
    "interview_scheduled": (
        "An interview has been scheduled as part of your application for "
        "<strong>{job_title}</strong>. Please check the "
        "<em>My Interviews</em> section of your dashboard for the date, "
        "time, and meeting details."
    ),
    "hired": (
        "Congratulations! We're delighted to offer you the "
        "<strong>{job_title}</strong> position. Our team will reach out "
        "with the details of your offer and onboarding shortly."
    ),
    "rejected": (
        "Thank you for taking the time to apply for the "
        "<strong>{job_title}</strong> position and for your interest in "
        "joining us. After careful consideration, we've decided to move "
        "forward with other candidates for this particular role. We "
        "encourage you to apply for future openings that match your "
        "profile."
    ),
    "applied": (
        "This is a quick note to confirm that your application for "
        "<strong>{job_title}</strong> has been received and is currently "
        "under review by our hiring team."
    ),
}


def _build_status_email_html(job_title: str, status: str) -> str:
    body = EMAIL_STATUS_COPY.get(
        status,
        "Your application status for <strong>{job_title}</strong> has "
        "been updated to <strong>{status}</strong>.",
    ).format(job_title=job_title, status=status.replace("_", " "))

    return f"""
    <div style="font-family: Arial, Helvetica, sans-serif; max-width: 480px; margin: 0 auto; color: #1e293b;">
      <div style="background: #4f46e5; padding: 20px 24px; border-radius: 10px 10px 0 0;">
        <span style="color: #ffffff; font-size: 18px; font-weight: 700;">HireTrack</span>
      </div>
      <div style="border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 10px 10px; padding: 24px;">
        <p style="font-size: 15px; line-height: 1.6; margin: 0 0 16px 0;">Hi,</p>
        <p style="font-size: 15px; line-height: 1.6; margin: 0 0 20px 0;">{body}</p>
        <p style="font-size: 15px; line-height: 1.6; margin: 0;">
          You can view the full details anytime from your
          <a href="#" style="color: #4f46e5; text-decoration: none; font-weight: 600;">HireTrack dashboard</a>.
        </p>
        <p style="font-size: 14px; line-height: 1.6; margin: 24px 0 0 0; color: #64748b;">
          Best regards,<br/>The HireTrack Team
        </p>
      </div>
    </div>
    """


def update_application_status(
    application_id: int,
    body,
    db: Session,
    current_user,
    background_tasks=None
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Recruiter only"
        )

    application = (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .join(Company, Job.company_id == Company.id)
        .filter(
            Application.id == application_id,
            Company.owner_id == current_user.id
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

    # Best-effort: notify the candidate (in-app + email). Never let a
    # notification/email failure break the status update itself.
    try:
        job = db.query(Job).filter(Job.id == application.job_id).first()
        candidate = db.query(User).filter(User.id == application.candidate_id).first()
        job_title = job.title if job else "the role"
        message = STATUS_MESSAGES.get(
            body.status, "Your application status was updated to {status}."
        ).format(job_title=job_title, status=body.status)

        create_notification(
            user_id=application.candidate_id,
            message=message,
            db=db,
            link=f"/candidate/applications/{application.id}/track"
        )

        if background_tasks is not None and send_email is not None and candidate and candidate.email:
            background_tasks.add_task(
                send_email,
                subject=f"Update on your {job_title} application",
                email=candidate.email,
                body=_build_status_email_html(job_title, body.status)
            )
    except Exception:
        # Notifications are a nice-to-have — swallow errors so the core
        # status-update action always succeeds.
        pass

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
            "job_location": job.location,
        })

    return result


def get_all_applications_for_recruiter(
    db: Session,
    current_user
):
    """All applicants across every vacancy owned by this recruiter —
    used by the "All Candidates" list, joined with Job (title),
    User (candidate name/email) and CandidateProfile (phone/photo)."""

    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Recruiter only"
        )

    rows = (
        db.query(Application, Job, User, CandidateProfile)
        .join(Job, Application.job_id == Job.id)
        .join(Company, Job.company_id == Company.id)
        .join(User, Application.candidate_id == User.id)
        .outerjoin(
            CandidateProfile,
            CandidateProfile.user_id == Application.candidate_id
        )
        .filter(Company.owner_id == current_user.id)
        .order_by(Application.applied_at.desc())
        .all()
    )

    result = []
    for application, job, user, profile in rows:
        result.append({
            "id": application.id,
            "status": application.status,
            "applied_at": application.applied_at,
            "job_id": application.job_id,
            "job_title": job.title,
            "candidate_id": application.candidate_id,
            "candidate_name": user.full_name,
            "candidate_email": user.email,
            "candidate_phone": profile.phone if profile else None,
            "candidate_photo_url": profile.photo_url if profile else None,
            "resume_url": application.resume_url,
        })

    return result