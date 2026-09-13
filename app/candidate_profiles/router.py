from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.users.model import User

from app.candidate_profiles.schema import (
    CandidateProfileCreateSchema,
    CandidateProfileResponseSchema,
    CandidateProfileUpdateSchema,
    CandidateProfileWithUserSchema
)

from app.candidate_profiles.service import (
    create_profile,
    get_my_profile,
    update_profile,
    delete_profile,
    get_candidate_profile_for_recruiter,
)
from app.candidate_profiles.model import CandidateProfile


import uuid


router = APIRouter(
    prefix="/profile",
    tags=["Candidate Profile"]
)

from fastapi import UploadFile, File
from app.core.supabase import supabase
import uuid


@router.post(
    "/",
    response_model=CandidateProfileResponseSchema
)
def create(
    body: CandidateProfileCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return create_profile(
        body,
        db,
        current_user
    )


@router.get(
    "/me",
    response_model=CandidateProfileResponseSchema
)
def me(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_my_profile(
        db,
        current_user
    )



@router.get(
    "/candidate/{user_id}",
    response_model=CandidateProfileWithUserSchema
)
def get_candidate_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_candidate_profile_for_recruiter(
        user_id,
        db,
        current_user
    )


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    extension = file.filename.split(".")[-1]
    file_name = f"{current_user.id}_{uuid.uuid4()}.{extension}"

    # Read file
    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    print(f"File Name: {file.filename}")
    print(f"Content Type: {file.content_type}")
    print(f"File Size: {len(content)} bytes")

    try:
        supabase.storage.from_("resumes").upload(
            path=file_name,
            file=content,
            file_options={
                "content-type": "application/pdf",
                "upsert": "true"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )

    resume_url = supabase.storage.from_("resumes").get_public_url(file_name)

    profile = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.user_id == current_user.id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Please create profile first."
        )

    profile.resume_url = resume_url
    db.commit()
    db.refresh(profile)

    return {
        "message": "Resume uploaded successfully.",
        "resume_url": resume_url
    }

@router.post("/upload-photo")
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    extension = file.filename.split(".")[-1]

    file_name = (
        f"{current_user.id}_"
        f"{uuid.uuid4()}.{extension}"
    )

    content = await file.read()

    supabase.storage.from_(
        "profile-photos"
    ).upload(
        file_name,
        content
    )

    url = supabase.storage.from_(
        "profile-photos"
    ).get_public_url(file_name)

    profile = (
        db.query(CandidateProfile)
        .filter(
            CandidateProfile.user_id
            == current_user.id
        )
        .first()
    )

    profile.photo_url = url

    db.commit()

    return {
        "photo_url": url
    }

@router.patch("/")
def update(
    body: CandidateProfileUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return update_profile(
        body,
        db,
        current_user
    )


@router.delete("/")
def delete(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return delete_profile(
        db,
        current_user
    )