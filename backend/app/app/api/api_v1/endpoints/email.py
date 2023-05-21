from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.job_offer import JobOffer
from sqlalchemy import func

from app.utilities.email import send_email

router = APIRouter()

@router.post("/")
def create_email(
    *,
    db: Session = Depends(deps.get_db),
    email: schemas.EmailContent,
) -> Any:
    """
    Send email
    """
    
    send_email(email.provider, email.title, email.email_text)
    return JSONResponse({})
