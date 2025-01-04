from fastapi import APIRouter, HTTPException
from models.users_model import User
from controller.user_controller import create_user, get_all_users;

router = APIRouter()

@router.get('/')
def get_users():
    try:
        result = get_all_users();
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting users")

@router.get('/{id}')
def get_user(user: User, id: str):
    return {"accepted":"Users"};

@router.post('/')
def save_user(user: User):
    print("New user received", user)
    try:
        result = create_user(user)  
        return result
    except ValueError as e:  
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid user data")  # Si los datos son inválidos
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")
    

@router.put('/{id}')
def update_user(user: User):
    return {"acepted":"Users"};

@router.delete('/{id}')
def delete_user(user: User):
    return {"acepted":"Users"};