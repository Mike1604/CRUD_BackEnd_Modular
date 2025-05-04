from fastapi import HTTPException
from db.db import db
from models.stats_model import StudySession;

statsCollection = db.get_collection("stats")

def get_study_sessions(userId: str):
    try:
        stats = list(statsCollection.find({"user_id": userId}))

        for stat in stats:
            stat["id"] = str(stat["_id"])  
            del stat["_id"]
        return stats
    except Exception as e:
        print(f"Error getting study sessions: {e}")
        raise

def record_study_session(data : StudySession):
    session_doc = data.model_dump()
    insert_result = statsCollection.insert_one(session_doc)

    if not insert_result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to save study session")
