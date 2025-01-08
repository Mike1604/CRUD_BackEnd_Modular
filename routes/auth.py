from fastapi import APIRouter, HTTPException
from models.auth_models import AuthRequest
from models.users_model import User, UpdateUser
from controller.user_controller import get_user_by_email
from controller.auth import verify_password

router = APIRouter()

@router.post('/login')
def login(req: AuthRequest):
    print("New login request received:", req)

    user = get_user_by_email(req.email)
    if not user or not verify_password(req.password, user.get("password")):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "message": "Login successful",
        "user_id": user["id"],
    }

@router.post('/logout')
def get_user(id: str):
    try:
        result = get_user_by_email(id);
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting users")