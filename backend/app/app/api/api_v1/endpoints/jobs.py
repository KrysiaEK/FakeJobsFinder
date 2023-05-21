from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.job_offer import JobOffer
from sqlalchemy import func

router = APIRouter()


@router.get("/stats")
def read_jobs(
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve job offers.
    """
    result = db.query(JobOffer.provider, func.count(JobOffer.provider)).group_by(JobOffer.provider).all()
    provider_counts = {provider: count for provider, count in result}

    result = db.query(JobOffer.score, func.count(JobOffer.score)).group_by(JobOffer.score).all()
    scores_counts = {f'group_{group}': count for group, count in result}

    return JSONResponse([
        provider_counts,
        scores_counts
    ])


@router.post("/", response_model=schemas.JobOffer)
def create_job_offer(
    *,
    db: Session = Depends(deps.get_db),
    job_in: schemas.JobOfferCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),    
) -> Any:
    """
    Create new job offer.
    """
    job = crud.job_offer.get_by_url(db, url=job_in.url)
    if job:
        raise HTTPException(
            status_code=400,
            detail="Job offer with this URL already exists.",
        )
    job = crud.job_offer.create(db, obj_in=job_in)
    return job


@router.put("/{id}", response_model=schemas.JobOffer)
def update_job_offer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    job_in: schemas.JobOfferUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update job offer.
    """
    job = crud.job_offer.get(db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job offer not found")
    job = crud.job_offer.update(db, db_obj=job, obj_in=job_in)
    return job


@router.get("/{id}", response_model=schemas.JobOffer)
def read_job_offer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get job offer by ID.
    """
    job = crud.job_offer.get(db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job offer not found")
    return job

@router.get("/{id}/image", response_model=schemas.JobOffer)
def read_job_offer_image(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get job offer by ID.
    """
    job = db.query(JobOffer).filter(JobOffer.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job offer not found")

    if not job.website_copy:
        raise HTTPException(status_code=404, detail="Job offer image not found")

    return StreamingResponse(iter([job.website_copy]), media_type="image/png")


@router.get("/", response_model=List[schemas.JobOffer])
def read_jobs(
    *,
    db: Session = Depends(deps.get_db),
    _start: int = 0,
    _end: int = 100,
    response: Response
) -> Any:
    """
    Retrieve job offers.
    """
    jobs = crud.job_offer.get_multi(db, skip=_start, limit=_end-_start)
    total_count = db.query(JobOffer).count()
    response.headers["X-Total-Count"] = str(total_count)
    return jobs


@router.delete("/{id}", response_model=schemas.JobOffer)
def delete_job_offer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a job offer.
    """
    job = crud.job_offer.get(db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job offer not found")
    job = crud.job_offer.remove(db, id=id)
    return job
