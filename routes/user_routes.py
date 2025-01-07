from fastapi import APIRouter, HTTPException
from models.users_model import User, UpdateUser
from controller.user_controller import create_user, get_all_users, get_user_by_id, update_user_by_id;

router = APIRouter()

@router.get('/')
def get_users():
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
    

@router.put("/{user_id}")
def update_user(user_id: str, updates: UpdateUser):
    user = get_user_by_id(user_id)  
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = updates.model_dump(exclude_unset=True)
    
    user.update(update_data)

    update_user_by_id(user)  
    
    return {"message": "User updated successfully", "user": user}

@router.delete('/{id}')
def delete_user(user: User):
    return {"acepted":"Users"};