from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None 
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    profile_picture_path: Optional[str] = None

class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    profile_picture_path: Optional[str] = None
