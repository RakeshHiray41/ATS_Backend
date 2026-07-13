from sqlalchemy.orm import Session

from app.companies.model import Company


def create_company(
    body,
    db: Session,
    current_user
):
    company = Company(
        name=body.name,
        description=body.description,
        website=body.website,
        location=body.location,
        owner_id=current_user.id
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company

def update_company(
    company_id: int,
    body,
    db: Session,
    current_user
):
    company = (
        db.query(Company)
        .filter(
            Company.id
            == company_id
        )
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    data = body.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(
            company,
            key,
            value
        )

    db.commit()
    db.refresh(company)

    return company

def delete_company(
    company_id: int,
    db: Session,
    current_user
):
    company = (
        db.query(Company)
        .filter(
            Company.id
            == company_id
        )
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    db.delete(company)
    db.commit()

    return {
        "message":
        "Company deleted"
    }
def get_my_company(
    db: Session,
    current_user
):
    company = (
        db.query(Company)
        .filter(Company.owner_id == current_user.id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found. Please create one first."
        )

    return company