from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from controller.user_controller import get_user_by_email
from controller.auth import verify_password, create_jwt
from models.users_model import Token

router = APIRouter()

@router.post('/login', response_model=Token)
def login(auth_request: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_by_email(auth_request.username)

    # Validate password
    if not user or not verify_password(auth_request.password, user.get("password")):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Generate token
    access_token = create_jwt({"sub": user["id"]})
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post('/logout')
def get_user(id: str):
    try:
        result = get_user_by_email(id);
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting users")