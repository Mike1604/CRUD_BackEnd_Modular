from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import Optional
from models.users_model import User, UpdateUser
from controller.user_controller import create_user, get_all_users, get_user_by_id, update_user_by_id, update_user_pic;

router = APIRouter()

@router.get('/')
def get_users():
    try:
        result = get_all_users()
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting users")

@router.get('/{user_id}')
def get_user(user_id: str):  
    try:
        result = get_user_by_id(user_id) 

        if "profile_picture_path" in result:
            result["profile_picture_path"] = f"http://localhost:8001{result['profile_picture_path']}"

        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting user")

@router.post('/')
def save_user(user: User):
    print("New user received", user)
    try:
        result = create_user(user)  
        return result
    except ValueError as e:  
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid user data")  
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")
    

@router.put("/{user_id}")
def update_user_data(
    user_id: str, 
    updates: UpdateUser  
):
    user = get_user_by_id(user_id)  

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = updates.model_dump(exclude_unset=True)  

    print(update_data)

    user.update(update_data)

    update_user_by_id(user)  

    return {"message": "User updated successfully", "user": user}

@router.put("/{user_id}/profile-picture")
def update_profile_picture(user_id: str, profile_picture: UploadFile = File(...)):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_pic_path = update_user_pic(profile_picture, user_id)
    user["profile_picture_path"] = new_pic_path
    update_user_by_id(user)

    return {"message": "Profile picture updated successfully", "profile_picture_path": new_pic_path}

@router.delete('/{id}')
def delete_user(user: User):
    return {"acepted":"Users"}