from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from models.group_models import AddMemberRequest, Group, GroupPost, UpdateGroupData
from controller.group_controller import add_group_post, get_all_group_posts, get_all_groups, create_group, remove_group_post, update_group_pic, update_group_by_id, get_group_by_id, delete_group_by_id, delete_group_pic, add_member, remove_member

router = APIRouter()

##Todo: update with JWT user id instead of endpoint
@router.get('/{userId}')
def get_groups(userId: str):
    try:
        result = get_all_groups(userId)

        for group in result:
            if "group_picture_path" in group:
                if group["group_picture_path"] != None:
                    group["group_picture_path"] = f"http://localhost:8001{group['group_picture_path']}"

        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting groups")


@router.get('/group/{group_id}')
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
            update_group_by_id(group['id'], group)
        else:
            group["group_picture_path"] = None
            print("No profile picture provided")

        group["group_picture_path"] = f"http://localhost:8001{group['group_picture_path']}"
        
        return {"message": "Group created successfully", "groupdata": group,}
    except ValueError as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid group data")  
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error creating group")
    
@router.put('/{groupId}')
def update_group(
    groupId: str,
    group_name: Optional[str] = Form(...), 
    group_description: Optional[str] = Form(None), 
    group_picture: Optional[UploadFile] = File(None)
):
    try:
        group_db = get_group_by_id(groupId)
        if not group_db:
            raise HTTPException(status_code=404, detail="Group not found")

        group_update = UpdateGroupData(group_name=group_name, group_description=group_description)
        group_dict = group_update.model_dump()

        if group_picture:
            picture_path = update_group_pic(group_picture, groupId)
            group_dict["group_picture_path"] = picture_path

        updated_group = update_group_by_id(groupId, group_dict)

        updated_group["group_picture_path"] = f"http://localhost:8001{updated_group['group_picture_path']}"

        return {
            "message": "Group updated successfully",
            "groupdata": updated_group,
        }
    
    except HTTPException as e:
        raise e  
    except ValueError as e:
        print(f"Validation Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid group data")

    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail="Error updating group")
    

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
    
@router.post("/{group_id}/members")
def add_member_to_group(group_id: str, request: AddMemberRequest):
    try:
        return add_member(group_id, request.user_id)
    except Exception as e:
        print(f"Error adding member to group: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    
@router.delete("/{group_id}/members")
def remove_member_from_group(group_id: str, request: AddMemberRequest):
    try:
        return remove_member(group_id, request.user_id)
    except Exception as e:
        print(f"Error removing member from group: {e}")
        raise HTTPException(status_code=500, detail="Database error")


@router.get('/{group_id}/posts')
def get_group_posts(group_id: str):
    try:
        return get_all_group_posts(group_id)
    except Exception as e:
        print(f"Error while getting group posts: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@router.post('/{group_id}/posts')
def create_group_post(group_id: str, post: GroupPost):
    try:
        return add_group_post(group_id, post)
    except Exception as e:
        print(f"Error adding a group post: {e}")
        raise HTTPException(status_code=500, detail="Database error")

##Use JWT to make sure the owner of the group is the one who is deleting the post
@router.delete('/{group_id}/posts')
def delete_group_post(group_id: str, post_id: str):
    try:
        return remove_group_post(group_id, post_id)
    except Exception as e:
        print(f"Error while removing a group post: {e}")
        raise HTTPException(status_code=500, detail="Database error")
