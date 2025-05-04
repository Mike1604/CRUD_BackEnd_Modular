from pydantic import BaseModel
from datetime import datetime

class StudySession(BaseModel):
    user_id: str
    deck: str
    language: str
    session_duration_minutes: float
    flashcards_studied: int 
    correct_answers: int 
    incorrect_answers: int 
    session_date: datetime 
