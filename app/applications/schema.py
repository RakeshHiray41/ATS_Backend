from pydantic import BaseModel
from datetime import datetime


class ApplicationResponseSchema(BaseModel):
    id: int
    status: str
    applied_at: datetime
    job_id: int
    candidate_id: int
    resume_url: str

    model_config = {
        "from_attributes": True
    }


# Used specifically for the recruiter's "Applicants" list,
# where candidate name/email is needed alongside application data.
class ApplicationWithCandidateSchema(ApplicationResponseSchema):
    candidate_name: str
    candidate_email: str


# Used specifically for the candidate's "My Applications" list,
# where the job title is needed alongside application data.
class ApplicationWithJobSchema(ApplicationResponseSchema):
    job_title: str
    job_location: str | None = None


# Used specifically for the recruiter's "All Candidates" list (across every
# vacancy they own), where job title, candidate contact number and photo
# are needed alongside application data.
class ApplicationWithCandidateAndJobSchema(ApplicationWithCandidateSchema):
    job_title: str
    candidate_phone: str | None = None
    candidate_photo_url: str | None = None


class UpdateApplicationStatusSchema(BaseModel):
    status: str