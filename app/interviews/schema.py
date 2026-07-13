from pydantic import BaseModel
from datetime import datetime


class InterviewCreateSchema(BaseModel):
    application_id: int
    interview_date: datetime
    meeting_link: str
    notes: str | None = None


class InterviewUpdateSchema(BaseModel):
    interview_date: datetime | None = None
    meeting_link: str | None = None
    status: str | None = None
    notes: str | None = None


class InterviewResponseSchema(BaseModel):
    id: int
    application_id: int
    interview_date: datetime
    meeting_link: str
    status: str
    notes: str | None

    model_config = {
        "from_attributes": True
    }


# Used for recruiter's job-wise interview list and candidate's "my interviews" list,
# where candidate name/email, job title, and company name are needed alongside interview data.
class InterviewWithDetailsSchema(InterviewResponseSchema):
    candidate_name: str
    candidate_email: str
    job_title: str
    company_name: str