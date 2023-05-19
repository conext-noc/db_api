from django.contrib.auth.hashers import make_password
from db_api.models import User


def add_user(email, password):
    hashed_password = make_password(password)
    user = User(email=email, password=hashed_password)
    user.save()
    user = get_user_by_email(email)
    if user["message"] == "success":
        return {
            "id": user["id"],
            "email": user["email"],
            "message": "User added successfully!",
        }
    return {"id": None, "email": None, "message": "An Error occurred!"}


# Usage example:
# add_user("example@example.com", "password123")


def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        return {
            "id": user.id,
            "email": user.email,
            "password": user.password,
            "message": "success",
        }
    except User.DoesNotExist:
        return {"id": None, "email": None, "message": "An Error occurred!"}


# Usage example:
# user = get_user_by_email("example@example.com")
# if user:
#     print(f"User ID: {user.id}, Email: {user.email}")
