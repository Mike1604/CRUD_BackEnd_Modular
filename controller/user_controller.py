from models.users_model import User;
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

def create_user(user: User):
    try:
        print("Trying to insert user")
        user_data = user.model_dump()

        user_data.pop("id", None)
        
        result = collection.insert_one(user_data)
        
        if result.acknowledged:
            print(f"Insert result: {result.inserted_id}")
            return {"message": "User created successfully", "id": str(result.inserted_id)}
        else:
            raise ValueError("Failed to insert the user.")
    except Exception as e:
        print(f"Error creating user: {e}")
        raise



