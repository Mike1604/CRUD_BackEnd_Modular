import shutil
from fastapi import HTTPException, File, UploadFile
from models.users_model import User;
from models.users_model import UpdateUser;
from bson import ObjectId
from db.db import db;
import os

collection = db.get_collection("users")
UPLOAD_DIR = os.path.join(os.getcwd(), "public")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

ALLOWED_IMAGE_EXTENSIONS = {"image/jpeg", "image/png"}

def get_all_users():
    try:
        users = list(collection.find())

        for user in users:
            user["id"] = str(user["_id"])  
            del user["_id"]
            del user["password"]
            del user["role"]
        return users
    except Exception as e:
        print(f"Error getting users: {e}")
        raise

def get_user_by_id(id: str):
    try:
        id_mongo = ObjectId(id)
        user = collection.find_one({"_id":id_mongo})

        if user is None:
            raise ValueError(f"No user found with id: {id}")

        user["id"] = str(user["_id"]) 
        del user["_id"]
        del user["password"]
        del user["role"]
        
        return user
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        raise

def get_user_by_email(email: str):
    try:
        user = collection.find_one({"email": email})

        if user is None:
            return None

        user["id"] = str(user["_id"])
        del user["_id"]
        
        return user
    except Exception as e:
        print(f"Error getting user by email: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    
def get_users_by_email(email: str):
    try:
        users = collection.find({"email": {"$regex": f"^{email}", "$options": "i"}}).limit(5)

        users = list(users)

        for user in users:
            user["id"] = str(user["_id"]) 
            del user["_id"]
            del user["password"]
            del user["role"]

        return users
    except Exception as e:
        print(f"Error getting user by email: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    
def get_users_by_batch(userIds):
    print("Getting batch of users")
    try:
        user_object_ids = [ObjectId(uid) for uid in userIds]

        users_cursor = collection.find({"_id": {"$in": user_object_ids}})
        users = list(users_cursor)

        for user in users:
            user["id"] = str(user["_id"]) 
            del user["_id"]
            del user["password"]
            del user["role"]

        return users
    except Exception as e:
        print(f"Error getting user by batch: {e}")
        raise HTTPException(status_code=500, detail="Database error")


def create_user(user: User):
    try:
        print("Trying to insert user")
        user_data = user.model_dump()

        user_data.pop("id", None)
        user_data["role"] = "user"
        
        result = collection.insert_one(user_data)
        
        if result.acknowledged:
            print(f"Insert result: {result.inserted_id}")
            return {"message": "User created successfully", "id": str(result.inserted_id)}
        else:
            raise ValueError("Failed to insert the user.")
    except Exception as e:
        print(f"Error creating user: {e}")
        raise

def update_user_by_id(user):
    try:
        print("Trying to update user")

        print(str(user))
        print(user["id"])
        
        id_mongo = ObjectId(user["id"])

        del user["id"]
        
        result = collection.update_one(
            {"_id": id_mongo}, 
            {"$set": user}  
        )
        
        if result.matched_count > 0:
            print(f"User with id {str(id_mongo)} updated successfully")
        else:
            print(f"No user found with id {id}")
            
    except Exception as e:
        print(f"Error updating user: {e}")
        raise

def update_user_pic(profile_picture: UploadFile, user_id: str):
    file_extension = profile_picture.filename.split(".")[-1]
    if profile_picture.content_type not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    file_location = os.path.join(UPLOAD_DIR, f"{user_id}.{file_extension}")

    with open(file_location, "wb") as f:
        shutil.copyfileobj(profile_picture.file, f)

    return f"/public/{user_id}.{file_extension}"