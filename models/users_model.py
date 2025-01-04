from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class User(BaseModel):
    id: Optional[str] = None 
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    role: Literal['superuser', 'alumno', 'admin']
    profile_picture_path: Optional[str] = None
    cu: str
