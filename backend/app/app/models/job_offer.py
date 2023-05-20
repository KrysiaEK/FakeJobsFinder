from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Column, LargeBinary, DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base

class JobOffer(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(index=True)
    url: Mapped[str] = mapped_column(unique=True)

    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    company: Mapped[str] = mapped_column()
    date = Column(DateTime)

    positives: Mapped[str] = mapped_column()
    negatives: Mapped[str] = mapped_column()
    positive_keywords: Mapped[str] = mapped_column()
    negative_keywords: Mapped[str] = mapped_column()

    score: Mapped[int] = mapped_column()

    email_text: Mapped[str] = mapped_column()
    website_copy = Column(LargeBinary, nullable=True, default=None)

    assigned_score: Mapped[Optional[int]] = mapped_column(default=None)
    created_at = Column(DateTime, default=func.now())