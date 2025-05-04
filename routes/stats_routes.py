from fastapi import APIRouter, Depends, HTTPException
from controller.stats_controller import get_study_sessions, record_study_session
from models.stats_model import StudySession
from controller.auth import verify_token

router = APIRouter()

@router.get('/study-session')
def get_users(userId: str = Depends(verify_token)):
    try:
        return get_study_sessions(userId)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting users")
    

@router.post("/study-session")
async def add_study_session(session: StudySession, userId: str = Depends(verify_token)):
    try:
        record_study_session(session)
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error recording a study session")

    return {"message": "Study session recorded"}
