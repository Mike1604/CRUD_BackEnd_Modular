from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None 
    email: EmailStr
    first_name: str
    last_name: str
    primary_language: str
    secondary_language: str
    password: str
    profile_picture_path: Optional[str] = None

class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    primary_language: Optional[str] = None
    secondary_language: Optional[str] = None
    password: Optional[str] = None
