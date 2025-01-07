from fastapi import APIRouter, HTTPException
from models.users_model import User, UpdateUser
from controller.user_controller import create_user, get_all_users, get_user_by_id, update_user_by_id;

router = APIRouter()

@router.get('/')
def login():
    try:
        result = get_all_users();
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting users")

@router.get('/{user_id}')
def get_user(id: str):
    try:
        result = get_user_by_id(id);
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting users")