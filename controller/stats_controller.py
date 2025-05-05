from fastapi import HTTPException
from db.db import db
from models.stats_model import GroupStudySession, StudySession;

statsCollection = db.get_collection("stats")
groupStatsCollection = db.get_collection("group_stats")

def get_all_study_sessions():
    try:
        stats = list(statsCollection.find())

        for stat in stats:
            stat["id"] = str(stat["_id"])  
            del stat["_id"]
        return stats
    except Exception as e:
        print(f"Error getting all study sessions: {e}")
        raise

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

def record_study_session(data : StudySession, userId : str):
    session_doc = data.model_dump()
    session_doc["user_id"] = userId
    insert_result = statsCollection.insert_one(session_doc)

    if not insert_result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to save study session")

def get_group_study_sessions(groupId:str):
    try:
        stats = list(groupStatsCollection.find({"group_id": groupId}))

        for stat in stats:
            stat["id"] = str(stat["_id"])  
            del stat["_id"]
        return stats
    except Exception as e:
        print(f"Error getting study sessions: {e}")
        raise

def record_group_study_session(data : GroupStudySession, userId : str, groupId: str):
    session_doc = data.model_dump()
    session_doc["group_id"] = groupId
    session_doc["user_id"] = userId
    insert_result = groupStatsCollection.insert_one(session_doc)

    if not insert_result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to save group study session")

