from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.users.router import router as user_router
from app.companies.router import router as company_router
from app.jobs.router import router as job_router
from app.candidate_profiles.router import router as profile_router
from app.applications.router import router as application_router
from app.interviews.router import router as interview_router
from app.dashboard.router import router as dashboard_router




app = FastAPI(
    title="HireFlow ATS API"
)

app.include_router(user_router)

app.include_router(company_router)

app.include_router(job_router)

app.include_router(profile_router)

app.include_router(application_router)

app.include_router(interview_router)

app.include_router(dashboard_router)


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "HireFlow ATS API"
    }