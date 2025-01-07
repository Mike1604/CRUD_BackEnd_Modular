from models.users_model import User;
from models.users_model import UpdateUser;
from bson import ObjectId
from db.db import db;

collection = db.get_collection("users");

def get_all_users():
    try:
        users = list(collection.find())

        for user in users:
            user["id"] = str(user["_id"])  
            del user["_id"]
        return users
    except Exception as e:
        print(f"Error getting users: {e}")
        raise

def get_user_by_id(id: str):
    try:
        id_mongo = ObjectId(id);
        user = collection.find_one({"_id":id_mongo})

        user["id"] = str(user["_id"]) 
        del user["_id"]
        
        return user
    except Exception as e:
        print(f"Error getting user: {e}")
        raise

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



