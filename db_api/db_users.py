from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
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
def update_user(data):
    try:
        hashed_password = make_password(data["new_passwd"])
        user = User.objects.get(email=data["email"])
        correct_passwd = check_password(data["old_passwd"], user.password)
        if not correct_passwd:
            return {
                "id": None,
                "email": None,
                "message": "An Error occurred!, either the password is wrong or that user does not exists!",
                "error": True,
            }
        user.password = hashed_password
        message = f"Success!, now user : [{user.email}] has the password changed to [{data['new_passwd']}]"
        if data.get("user_type") != None and data.get("user_type") != "":
            user.user_type = data.get("user_type")
            message += f", now now user : [{user.email}] has the password changed to [{data.get('user_type')}]"
        user.save()
        return {
            "message": message,
            "user": user.email,
            "user_type": user.user_type,
            "new_passwd": data["new_passwd"],
            "old_passwd": data["old_passwd"],
        }
    except User.DoesNotExist:
        return {
            "id": None,
            "email": None,
            "message": "An Error occurred!",
            "error": True,
        }


# DELETE
def delete_user(email, user_type):
    print(email, user_type)
    return {"message": "success"}
