import shutil
import datetime
from fastapi import HTTPException, UploadFile
from pymongo import ReturnDocument
from models.users_model import User;
from models.group_models import Group, GroupMember, GroupPost, RoleEnum;
from controller.user_controller import get_user_by_id
from bson import ObjectId
from db.db import db;
import os

groupCollection = db.get_collection("groups")
groupPostCollection = db.get_collection("group_posts")
UPLOAD_DIR = os.path.join(os.getcwd(), "public/groups_profile")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

ALLOWED_IMAGE_EXTENSIONS = {"image/jpeg", "image/png"}

#Todo: update with owned groups
def get_all_groups(user_id: str):
    try:
        groups = list(groupCollection.find({
            "$or": [
                {"owner": user_id},  
                {"members.user_id": user_id}  
            ]
        }))

        for group in groups:
            group["id"] = str(group["_id"])  
            del group["_id"]
            del group["members"]
        
        return groups
    except Exception as e:
        print(f"Error getting groups: {e}")
        raise


def get_group_by_id(id: str):
    try:
        id_mongo = ObjectId(id)
        user = groupCollection.find_one({"_id":id_mongo})

        if user is None:
            raise ValueError(f"No group found with id: {id}")

        user["id"] = str(user["_id"]) 
        del user["_id"]
        
        return user
    except Exception as e:
        print(f"Error getting group by ID: {e}")
        raise

def create_group(group: Group):
    try:
        print("Trying to insert a new group")
        group_data = group.model_dump()

        owner = get_user_by_id(group_data["owner"])

        member = GroupMember(
            user_id=owner["id"],  
            role=RoleEnum.admin,        
            since=datetime.datetime.now(datetime.timezone.utc)
        )

        group_data["members"] = [member.model_dump()]

        group_data["group_picture_path"] = None

        result = groupCollection.insert_one(group_data)

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
    relative_path = image_path.lstrip("/") 
    path = os.path.join(os.getcwd(), relative_path)
    print("Path trying ", path)
    if os.path.exists(path):  
        os.remove(path)
        print(f"Imagen eliminada: {image_path}")
    else:
        print("Imagen no encontrada en el servidor")



def delete_group_by_id(groupId: str):
    delete_result = groupCollection.delete_one({"_id": ObjectId(groupId)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete group")

    return {"message": "Group deleted successfully"}

def update_group_by_id(group_id: str, updated_data: dict):
    try:
        print(f"Trying to update group {group_id}")
        
        id_mongo = ObjectId(group_id)
        
        result = groupCollection.update_one(
            {"_id": id_mongo}, 
            {"$set": updated_data}  
        )
        
        if result.matched_count > 0:
            print(f"Group with id {group_id} updated successfully")
            return get_group_by_id(group_id)  
        else:
            print(f"No group found with id {group_id}")
            return None  
            
    except Exception as e:
        print(f"Error updating group: {e}")
        raise

def add_member(groupId, userId):
    group_object_id = ObjectId(groupId)
    
    group = groupCollection.find_one({"_id": group_object_id})
    
    if not group:
         raise HTTPException(status_code=404, detail="Group not found")

    if any(member["user_id"] == userId for member in group["members"]):
        raise HTTPException(status_code=400, detail="User is already a member")

    new_member = GroupMember(
        user_id=userId,  
        role=RoleEnum.usuario,        
        since=datetime.datetime.now(datetime.timezone.utc)
    )

    result = groupCollection.find_one_and_update(
        {"_id": group_object_id},
        {"$addToSet": {"members": new_member.model_dump()}},
        return_document=ReturnDocument.AFTER  
    )
    
    memberDict = new_member.model_dump()
    new_member_added = None
    if result:
        for member in result.get('members', []):
            if member['user_id'] == memberDict['user_id']:
                new_member_added = member
                break

    if new_member_added:
        return {"status": "success", "new_member": new_member_added}
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to add member")

def remove_member(groupId:str, userId:str):
    group_object_id = ObjectId(groupId)
    
    group = groupCollection.find_one({"_id": group_object_id})
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group["owner"] == userId:
        raise HTTPException(status_code=400, detail="Owner cannot be removed from the group")
    
    if not any(member["user_id"] == userId for member in group["members"]):
        raise HTTPException(status_code=400, detail="User is not a member of the group")
    
    result = groupCollection.update_one(
        {"_id": group_object_id},
        {"$pull": {"members": {"user_id": userId}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to remove member")

    return {"message": "Member removed successfully"}

def get_all_group_posts(group_id: str):
    try:
        group_posts = list(groupPostCollection.find({"group_owner": group_id}).sort("created_at", -1))

        for group_post in group_posts:
            group_post["id"] = str(group_post["_id"])  
            del group_post["_id"]
        
        return group_posts
    except Exception as e:
        print(f"Error getting groups: {e}")
        raise

def add_group_post(group_id: str, userId: str, post: GroupPost):
    try:
        print("Trying to add a new group post")
        
        group_post = post.model_dump()
        group_post["post_owner"] = userId
        group_post["group_owner"] = group_id  
        group_post["created_at"] = datetime.datetime.now(datetime.timezone.utc)
        
        result = groupPostCollection.insert_one(group_post)

        if result.acknowledged:
            inserted_post = groupPostCollection.find_one({"_id": result.inserted_id})
            inserted_post["id"] = str(inserted_post.pop("_id"))

            return inserted_post  
        else:
            raise ValueError("Failed to add the post.")
    except Exception as e:
        print(f"Error creating post: {e}")
        raise
    
def get_group_post_by_id(post_id:str):
    try:
        id_mongo = ObjectId(post_id)
        result = groupPostCollection.find_one({"_id":id_mongo})

        if result is None:
            raise ValueError(f"No group post found with id: {id}")
        
        result["id"] = str(result["_id"])
        del result["_id"]
        
        return result;
    except Exception as e:
        print(f"Error trying to find post: {e}")
        raise
    
    
def remove_group_post(post_id: str):
    try:
        delete_result = groupPostCollection.delete_one({"_id": ObjectId(post_id)})

        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete group")
        
        return {"message": "Group post deleted successfully"}
    except Exception as e:
        print(f"Error creating post: {e}")
        raise