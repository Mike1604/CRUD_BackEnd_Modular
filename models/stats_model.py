from pydantic import BaseModel
from datetime import datetime

class StudySession(BaseModel):
    deck: str
    language: str
    session_duration_minutes: float
    flashcards_studied: int 
    correct_answers: int 
    incorrect_answers: int 
    session_date: datetime 

class GroupStudySession(BaseModel):
    group_id: str
    activity: str
    deck: str
    language: str
    session_duration_minutes: float
    flashcards_studied: int 
    correct_answers: int 
    incorrect_answers: int 
    session_date: datetime 