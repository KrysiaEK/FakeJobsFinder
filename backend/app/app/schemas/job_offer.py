from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class JobOfferBase(BaseModel):
    provider: str
    url: str
    title: str
    description: str
    author: str
    score: int
    positives: str
    negatives: str
    keywords: str
    email_text: str
    report_pdf: Optional[bytes]
    website_pdf: Optional[bytes]
    assigned_score: Optional[int]

class JobOfferCreate(JobOfferBase):
    pass

class JobOfferUpdate(JobOfferBase):
    pass

class JobOffer(JobOfferBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
