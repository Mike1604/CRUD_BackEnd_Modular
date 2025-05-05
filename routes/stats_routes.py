from fastapi import APIRouter, Depends, HTTPException
from controller.group_controller import get_group_by_id
from controller.stats_controller import get_all_study_sessions, get_group_study_sessions, get_study_sessions, record_group_study_session, record_study_session
from models.stats_model import GroupStudySession, StudySession
from controller.auth import verify_token

router = APIRouter()

@router.get('/')
def get_all_study_sessions_stats():
    try:
        return get_all_study_sessions()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting all study sessions")
    

@router.get('/study-session')
def get_study_sessions_stats(userId: str = Depends(verify_token)):
    try:
        return get_study_sessions(userId)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting study sessions")
    

@router.post("/study-session")
def add_study_session(session: StudySession, userId: str = Depends(verify_token)):
    try:
        record_study_session(session, userId)
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error recording a study session")

    return {"message": "Study session recorded"}

@router.get('/group-activity-session/{groupId}')
def get_group_study_sessions_stats(groupId: str, userId: str = Depends(verify_token)):
    try:
        group = get_group_by_id(groupId)
        
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        
        if group["owner"] != userId and userId not in [member["user_id"] for member in group["members"]]:
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        return get_group_study_sessions(groupId)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting study sessions")

@router.post("/group-activity-session")
def add_group_study_session(session: GroupStudySession, userId: str = Depends(verify_token)):
    try:
        record_group_study_session(session, userId)
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error recording a study session")

    return {"message": "Study session recorded"}
