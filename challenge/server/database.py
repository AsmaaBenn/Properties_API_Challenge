"""
Database connection file.

This script content Database CRUD Operations.
"""
import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.users

user_collection = database.get_collection("users_collection")


# helpers
def user_helper(user) -> dict:
    """For parsing the results from a database query into a Python dict."""
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "properties": user["properties"]
    }


# List all the users present in the database
async def retrieve_users():
    """
        List all the users.

    :return user_helper(user)
    :return list of users
    :rtype list
    """
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user
async def add_user(user_data: dict) -> dict:
    """
        Add a new user.

    :param user_data
    :return user_helper(user)
    :return list of users
    :rtype list
    """
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Add a new property of user with a matching ID
async def add_properties_to_user(id_user: str, user_data: dict) -> dict:
    """
        Create a new property for specific property.

    :param id_user, user_data
    :return user_helper(user)
    :return list of users
    :rtype list
    """
    user = await user_collection.find_one({"_id": ObjectId(id_user)})
    if user:
        user_properties = user["properties"]
        if user_properties:
            user_properties.append(user_data)
        else:
            user_properties = [user_data]
        add_property = await user_collection.update_one(
                {"_id": ObjectId(id_user)},
                {'$set': {'properties': user_properties}}
        )
        if add_property:
            new_user = await user_collection.find_one(
                {"_id": ObjectId(id_user)}
            )
            return user_helper(new_user)


# Retrieve a user with a matching ID
async def retrieve_user(id_user: str) -> dict:
    """
        List a data of user with matching ID.

    :param id_user
    :return user_helper(user)
    :return list of users
    :rtype list
    """
    user = await user_collection.find_one({"_id": ObjectId(id_user)})
    if user:
        return user_helper(user)


# Retrieve all properties of user with a matching ID
async def retrieve_user_properties(id_user: str) -> dict:
    """
        List all properties for a specific user.

    :param id_user
    :return properties
    :return list of properties
    :rtype list
    """
    user = await user_collection.find_one({"_id": ObjectId(id_user)})
    if user:
        properties = user["properties"]
        if properties:
            return properties
        return {'message': "this user doesn't have properties"}


# Update a User with a matching ID
async def update_user(id_user: str, data: dict):
    """
        Update data for a specific user.

    :param id_user, data
    :return updated_user
    :rtype pymongo.results.UpdateResult
    """
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id_user)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id_user)}, {"$set": data}
        )
        return updated_user


# Update a owner property with a matching ID_prop
async def update_prop_owner(id_prop: str, data: dict):
    """
        Update the owner property for a specific property.

    :param id_prop, data
    :return updated_user
    :rtype pymongo.results.UpdateResult
    """
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one(
        {"properties.id_proper": {"$in": [id_prop]}}
        )
    if user:
        id_user = user["_id"]
        updated_user_owner = await user_collection.update_one(
            {"_id": ObjectId(id_user)},
            {'$set': {'fullname': data["fullname"], 'email': data["email"]}}
        )
        return updated_user_owner


# Update a property data with a matching ID_prop
async def update_prop_data(id_prop: str, data: dict):
    """
        Update the property data for a specific property.

    :param id_prop, data
    :return updated_prop
    :rtype pymongo.results.UpdateResult
    """
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one(
        {"properties.id_proper": {"$in": [id_prop]}}
        )
    if user:
        if len(user["properties"]) > 1:
            i = 0
            for pro in user["properties"]:
                if pro["id_proper"] == id_prop:
                    break
                i += 1
            user["properties"][i] = data
        else:
            user["properties"][0] = data
        id_user = user["_id"]
        updated_prop = await user_collection.update_one(
            {"_id": ObjectId(id_user)},
            {'$set': {'properties': user["properties"]}}
        )
        return updated_prop


# Delete a User from the database
async def delete_user(id_user: str):
    """
        Delete user for a specific Id.

    :param id_user
    :return test if the user is deleted
    :rtype bool
    """
    user = await user_collection.find_one({"_id": ObjectId(id_user)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id_user)})
        return True


async def delete_property(id_prop: str):
    """
        Delete property for a specific Id_prop.

    :param id_prop
    :return test if the user is deleted
    :rtype bool
    """
    user = await user_collection.find_one(
        {"properties.id_proper": {"$in": [id_prop]}}
        )
    if user:
        if len(user["properties"]) > 1:
            i = 0
            for pro in user["properties"]:
                if pro["id_proper"] == id_prop:
                    break
                i += 1
            del user["properties"][i]
        else:
            user["properties"] = None
        id_user = user["_id"]
        user_collection.update_one(
            {"_id": ObjectId(id_user)},
            {'$set': {'properties': user["properties"]}}
        )
        return True
