"""
    This script is the User route.

This script content the End points.
"""
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import bson

from server.database import (
    retrieve_users,
    add_user,
    retrieve_user,
    retrieve_user_properties,
    add_properties_to_user,
    update_user,
    update_prop_owner,
    update_prop_data,
    delete_user,
    delete_property
)
from server.models.usersproperties import (
    ErrorResponseModel,
    ResponseModel,
    UsersPropertiesSchema,
    UpdateUsersPropertiesModel,
    PropertiesSchema,
    UpdateOwnerPropertiesModel
)

router = APIRouter()


@router.get("/", response_description="Users retrieved")
async def get_users():
    """
        List all the users.

    return list of users in database
    """
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "User data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.post("/", response_description="user data added into the database")
async def add_new_user(user: UsersPropertiesSchema = Body(...)):
    """
        Register new user.

    return the new user
    """
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.get("/{id_user}", response_description="User data retrieved")
async def get_user_data(id_user):
    """
        Get the data from a single user.

    return the new user
    """
    if not bson.objectid.ObjectId.is_valid(id_user):
        return ErrorResponseModel("An error occurred.", 400, "ID Not Valid.")
    user = await retrieve_user(id_user)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.get("/{id_user}/properties", response_description="User Properties")
async def get_user_properties(id_user):
    """
        List all properties from a user.

    return properties from user
    """
    if not bson.objectid.ObjectId.is_valid(id_user):
        return ErrorResponseModel("An error occurred.", 400, "ID Not Valid.")
    user = await retrieve_user_properties(id_user)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.post("/{id_user}/properties", response_description="add a property")
async def add_user_properties(id_user: str, data: PropertiesSchema = Body(...)):
    """
        Create a property.

    return the user with the new property
    """
    if not bson.objectid.ObjectId.is_valid(id_user):
        return ErrorResponseModel("An error occurred.", 400, "ID Not Valid.")
    user = jsonable_encoder(data)
    new_properties = await add_properties_to_user(id_user, user)
    if new_properties:
        return ResponseModel(new_properties, "Priperties added successfully.")
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the property owner.",
    )


@router.put("/{id_user}", response_description="Update properties to a user")
async def update_user_data(id_user: str, req: UpdateUsersPropertiesModel = Body(...)):
    """
        Update user data.

    return Response message
    """
    if not bson.objectid.ObjectId.is_valid(id_user):
        return ErrorResponseModel("An error occurred.", 400, "ID Not Valid.")
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id_user, req)
    if updated_user:
        return ResponseModel(
            "User Data with ID: {} update is successful".format(id_user),
            "User Data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.put("/properties/{id_prop}", response_description="Update property owner")
async def update_property_owner(id_prop: str, req: UpdateOwnerPropertiesModel = Body(...)):
    """
        Update property owner.

    return Response message
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_property_owner = await update_prop_owner(id_prop, req)
    if updated_property_owner:
        return ResponseModel(
            "Owner information with PropertyID: {} update is successful".format(id_prop),
            "Owner information updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the property owner.",
    )


@router.put("/properties/{id_prop}/data", response_description="add properties to a user")
async def update_property_data(id_prop: str, req: PropertiesSchema = Body(...)):
    """
        Update property data.

    return Response message
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_property_data = await update_prop_data(id_prop, req)
    if updated_property_data:
        return ResponseModel(
            "User with PropertyID: {} update is successful".format(id_prop),
            "User Data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/{id_user}", response_description="User data deleted from the database")
async def delete_user_data(id_user: str):
    """
        Delete a user.

    return Response message
    """
    if not bson.objectid.ObjectId.is_valid(id_user):
        return ErrorResponseModel("An error occurred.", 400, "ID Not Valid.")
    deleted_user = await delete_user(id_user)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id_user),
            "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "User with id {0} doesn't exist".format(id_user)
    )


@router.delete("/properties/{id_prop}", response_description="property deleted from the database")
async def delete_property_data(id_prop: str):
    """
        Delete a property.

    return Response message
    """
    deleted_property = await delete_property(id_prop)
    if deleted_property:
        return ResponseModel(
            "property with ID: {} removed".format(id_prop),
            "property deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "User with id {0} doesn't exist".format(id_prop)
    )
