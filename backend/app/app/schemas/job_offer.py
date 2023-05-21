from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class JobOfferBase(BaseModel):
    provider: str
    url: str
    title: str
    description: str
    author: str
    company: str
    positives: str
    negatives: str
    positive_keywords: str
    negative_keywords: str
    score: int
    email_text: str
    assigned_score: Optional[int] = None


# Properties to receive via API on creation
class JobOfferCreate(JobOfferBase):
    pass


# Properties to receive via API on update
class JobOfferUpdate(JobOfferBase):
    pass


# Properties to return via API
class JobOffer(JobOfferBase):
    id: int
    date: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# Properties stored in DB
class JobOfferInDB(JobOffer):
    pass

class JobOfferStats(BaseModel):
    services: list[dict]
    