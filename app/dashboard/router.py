from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from app.database.database import (
    get_db
)
from app.core.dependencies import (
    get_current_user
)

from app.dashboard.service import (
    recruiter_dashboard,
    candidate_dashboard
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/recruiter")
def recruiter(
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    return recruiter_dashboard(
        db,
        current_user
    )


@router.get("/candidate")
def candidate(
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    return candidate_dashboard(
        db,
        current_user
    )