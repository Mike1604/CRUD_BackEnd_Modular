from fastapi import APIRouter, Depends, HTTPException, File, Query, UploadFile
from controller.auth import verify_token
from models.users_model import User, UpdateUser, UserBatchRequest, Token
from controller.auth import create_jwt
from controller.user_controller import create_user, get_all_users, get_user_by_id, update_user_by_id, update_user_pic, get_users_by_batch, get_users_by_email;

router = APIRouter()

@router.get('/')
def get_users(user_id: str = Depends(verify_token)):
    try:
        result = get_all_users()
        
        for user in result:
            if "profile_picture_path" in user:
                user["profile_picture_path"] = f"http://localhost:8001{user['profile_picture_path']}"
        
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting users")

@router.get('/find-users-email')
def search_users_by_email(email: str = Query(..., min_length=1)):
    try: 
        users =  get_users_by_email(email)
        
        for user in users:
            if "profile_picture_path" in user:
                user["profile_picture_path"] = f"http://localhost:8001{user['profile_picture_path']}"
        
        return users
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")
    

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
    
@router.post("/batch")
def get_users_batch(request: UserBatchRequest):
    user_ids = request.user_ids
    
    if not user_ids:
        raise HTTPException(status_code=400, detail="La lista de IDs no puede estar vacía")
    
    try: 
        result =  get_users_by_batch(user_ids)
        
        for user in result:
            if "profile_picture_path" in user and user["profile_picture_path"] != None:
                user["profile_picture_path"] = f"http://localhost:8001{user['profile_picture_path']}"
        
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")
    
@router.post('/')
def save_user(user: User):
    print("New user received", user)
    try:    
        result = create_user(user)  
        # Generate token
        access_token = create_jwt({"sub": result["id"]})
        return Token(message="User created", access_token=access_token, token_type="bearer")
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