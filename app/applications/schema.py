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


class UpdateApplicationStatusSchema(BaseModel):
    status: str