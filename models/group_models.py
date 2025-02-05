from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional

class Group(BaseModel):
    group_name: str
    group_description: Optional[str] = None
    owner: str

class RoleEnum(str, Enum):
    admin = "Admin"
    usuario = "Usuario"

class GroupMember(BaseModel):
    user_id: str
    role: RoleEnum
    since: datetime
    
class AddMemberRequest(BaseModel):
    user_id: str
    
class UpdateGroupData(BaseModel):
    group_name: str
    group_description: Optional[str] = None
    
class GroupPost(BaseModel):
    text_content: str