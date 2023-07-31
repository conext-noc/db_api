from django.contrib.auth.hashers import make_password
from db_api.models import User


# HANDLER
def user_to_dict(user):
    result = {
        field: getattr(user, field)
        for field in [
            "id",
            "email",
            "password",
            "user_type",
        ]
    }
    return result


# CREATE
def add_user(email, password, user_type):
    hashed_password = make_password(password)
    user = User(email=email, password=hashed_password, user_type=user_type)
    user.save()
    user = get_user_by_email(email)
    if user["message"] == "success":
        return {
            "id": user["id"],
            "email": user["email"],
            "message": "User added successfully!",
            "error": False,
        }
    return {"id": None, "email": None, "message": "An Error occurred!", "error": True}


# READ
def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        returned_user = user_to_dict(user)
        returned_user["message"] = "success"
        return returned_user
    except User.DoesNotExist:
        return {
            "id": None,
            "email": None,
            "message": "An Error occurred!",
            "error": True,
        }


# UPDATE
def update_user(email, user_type):
    print(email, user_type)
    return {"message": "success"}


# DELETE
def delete_user(email, user_type):
    print(email, user_type)
    return {"message": "success"}
