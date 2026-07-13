from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.candidate_profiles.model import CandidateProfile


def _skills_to_db(skills):
    """Convert incoming skills (list or string) into a plain comma-separated
    string, since the `skills` column is a Text column, not a real array."""
    if skills is None:
        return None
    if isinstance(skills, list):
        return ", ".join(str(s).strip() for s in skills if str(s).strip())
    return str(skills).strip()


def create_profile(
    body,
    db: Session,
    current_user
):
    profile = (
        db.query(CandidateProfile)
        .filter(
            CandidateProfile.user_id
            == current_user.id
        )
        .first()
    )

    if profile:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists"
        )

    profile = CandidateProfile(
        phone=body.phone,
        bio=body.bio,
        skills=_skills_to_db(body.skills),
        experience=body.experience,
        linkedin_url=body.linkedin_url,
        github_url=body.github_url,
        user_id=current_user.id
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def get_my_profile(
    db: Session,
    current_user
):
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
            status_code=404,
            detail="Profile not found"
        )

    return profile


def update_profile(
    body,
    db: Session,
    current_user
):
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

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    data = body.model_dump(
        exclude_unset=True
    )

    if "skills" in data:
        data["skills"] = _skills_to_db(data["skills"])

    for key, value in data.items():
        setattr(
            profile,
            key,
            value
        )

    db.commit()
    db.refresh(profile)

    return profile


def delete_profile(
    db: Session,
    current_user
):
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

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    db.delete(profile)
    db.commit()

    return {
        "message":
        "Profile deleted"
    }