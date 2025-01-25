from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from models.group_models import Group
from controller.group_controller import get_all_groups, create_group, update_group_pic, update_group_by_id, get_group_by_id, delete_group_by_id, delete_group_pic

router = APIRouter()

@router.get('/')
def get_groups():
    try:
        result = get_all_groups()

        for group in result:
            if "group_picture_path" in group:
                if group["group_picture_path"] != None:
                    group["group_picture_path"] = f"http://localhost:8001{group['group_picture_path']}"

        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting groups")


@router.get('/{group_id}')
def get_group(group_id: str):  
    try:
        result = get_group_by_id(group_id) 

        if "group_picture_path" in result:
            if result["group_picture_path"] != None:
                result["group_picture_path"] = f"http://localhost:8001{result['group_picture_path']}"

        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting user")


@router.post('/')
def add_group(
    group_name: str = Form(...), 
    group_description: Optional[str] = Form(None), 
    owner: str = Form(...),
    group_picture: Optional[UploadFile] = File(None)  
):
    group = Group(group_name=group_name, group_description=group_description, owner=owner)
    print("New group received:", group)
    try:
        resultId = create_group(group)
        
        group = group.model_dump()

        group["id"] = str(resultId)

        if group_picture:
            picture_path = update_group_pic(group_picture, resultId)
            group["group_picture_path"] = picture_path
            update_group_by_id(group)
        else:
            group["group_picture_path"] = None
            print("No profile picture provided")

        return {"message": "Group created successfully", "groupdata": group,}
    except ValueError as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid user data")  
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")
    
@router.delete('/{group_id}')
def delete_group(group_id: str): 
    try:

        group = get_group_by_id(group_id)
        
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if "group_picture_path" in group and group["group_picture_path"]:
            image_path = group["group_picture_path"]
            delete_group_pic(image_path)

        return delete_group_by_id(group_id)
    except Exception as e:
        print(f"Error deleting group: {e}")
        raise HTTPException(status_code=500, detail="Error deleting group") 
