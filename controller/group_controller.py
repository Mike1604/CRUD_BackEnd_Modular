import shutil
import datetime
from fastapi import HTTPException, UploadFile
from models.users_model import User;
from models.group_models import Group, GroupMember, RoleEnum;
from controller.user_controller import get_user_by_id
from bson import ObjectId
from db.db import db;
import os

collection = db.get_collection("groups")
UPLOAD_DIR = os.path.join(os.getcwd(), "public/groups_profile")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

ALLOWED_IMAGE_EXTENSIONS = {"image/jpeg", "image/png"}

#Todo: update with owned groups
def get_all_groups():
    try:
        groups = list(collection.find())

        for group in groups:
            group["id"] = str(group["_id"])  
            del group["_id"]
            del group["members"]
        return groups
    except Exception as e:
        print(f"Error getting users: {e}")
        raise

def get_group_by_id(id: str):
    try:
        id_mongo = ObjectId(id)
        user = collection.find_one({"_id":id_mongo})

        if user is None:
            raise ValueError(f"No group found with id: {id}")

        user["id"] = str(user["_id"]) 
        del user["_id"]
        
        return user
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        raise

def create_group(group: Group):
    try:
        print("Trying to insert a new group")
        group_data = group.model_dump()

        owner = get_user_by_id(group_data["owner"])

        print(type(datetime.datetime.now(datetime.timezone.utc)))

        member = GroupMember(
            user_id=owner["id"],  
            role=RoleEnum.admin,        
            since=datetime.datetime.now(datetime.timezone.utc)
        )

        group_data["members"] = [member.model_dump()]

        group_data["group_picture_path"] = None

        result = collection.insert_one(group_data)

        if result.acknowledged:
            print(f"Insert result: {result.inserted_id}")
            return result.inserted_id
        else:
            raise ValueError("Failed to insert the user.")
    except Exception as e:
        print(f"Error creating group: {e}")
        raise

def update_group_pic(group_picture: UploadFile, groupId: str):
    file_extension = group_picture.filename.split(".")[-1]
    if group_picture.content_type not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    file_location = os.path.join(UPLOAD_DIR, f"{groupId}.{file_extension}")

    with open(file_location, "wb") as f:
        shutil.copyfileobj(group_picture.file, f)

    return f"/public/groups_profile/{groupId}.{file_extension}"


def delete_group_pic(image_path: str):
    relative_path = image_path.lstrip("/")  # Elimina la barra inicial si existe
    path = os.path.join(os.getcwd(), relative_path)
    print("Path trying ", path)
    if os.path.exists(path):  
        os.remove(path)
        print(f"Imagen eliminada: {image_path}")
    else:
        print("Imagen no encontrada en el servidor")



def delete_group_by_id(groupId: str):
    delete_result = collection.delete_one({"_id": ObjectId(groupId)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete group")

    return {"message": "Group deleted successfully"}

def update_group_by_id(group: Group):
    try:
        print("Trying to update group")
        
        id_mongo = ObjectId(group["id"])

        del group["id"]
        
        result = collection.update_one(
            {"_id": id_mongo}, 
            {"$set": group}  
        )
        
        if result.matched_count > 0:
            print(f"group with id {str(id_mongo)} updated successfully")
        else:
            print(f"No group found with id {id}")
            
    except Exception as e:
        print(f"Error updating group: {e}")
        raise

