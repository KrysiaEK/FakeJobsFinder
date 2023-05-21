from pydantic import BaseModel, EmailStr
from typing import List


class EmailContent(BaseModel):
    email_text: str
    provider: EmailStr
    title: str


class EmailValidation(BaseModel):
    email: EmailStr
    subject: str
    token: str

