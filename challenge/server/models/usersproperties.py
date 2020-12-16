"""This file define the Schema for which our data will be based on."""
from typing import Optional
from pydantic import BaseModel, EmailStr
from typing import List


class PropertiesSchema(BaseModel):
    """Schema of properties in user."""
    id_proper: str
    property_type: str
    description: str


class UsersPropertiesSchema(BaseModel):
    """Schema of user data in MongoDB database."""
    fullname: str
    email: EmailStr
    properties: List[PropertiesSchema] = None


class UpdateUsersPropertiesModel(BaseModel):
    """To update user."""
    fullname: Optional[str]
    email: Optional[EmailStr]
    properties: Optional[List[PropertiesSchema]]


class UpdateOwnerPropertiesModel(BaseModel):
    """To update Properties."""
    fullname: Optional[str]
    email: Optional[EmailStr]


def ResponseModel(data, message):
    """
        Response function when there is no error.

    return a dict that content  data + code +  message
    """
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def ErrorResponseModel(error, code, message):
    """
        Response function when there an error.

    return a dict that content  data + code +  message
    """
    return {
        "error": error,
        "code": code,
        "message": message
    }
