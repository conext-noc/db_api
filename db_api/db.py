from django.contrib.auth.hashers import make_password
from db_api.models import User, Client

# import os
# import re
# import json


def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        return {
            "id": user.id,
            "email": user.email,
            "password": user.password,
            "userType": user.userType,
            "message": "success",
        }
    except User.DoesNotExist:
        return {"id": None, "email": None, "message": "An Error occurred!"}


def get_client_by_contract(contract):
    try:
        client = Client.objects.get(contract=contract)

        returned_client = {
            field: getattr(client, field)
            for field in [
                "frame",
                "slot",
                "port",
                "onu_id",
                "name_1",
                "name_2",
                "contract",
                "status",
                "state",
                "last_down_cause",
                "last_down_time",
                "last_down_date",
                "sn",
                "device",
                "plan",
                "vlan",
                "fsp",
            ]
        }
        return {
            "client": returned_client,
            "message": "success",
        }
    except Client.DoesNotExist:
        return {"client": None, "message": "An Error occurred!"}


def add_user(email, password, userType):
    hashed_password = make_password(password)
    user = User(email=email, password=hashed_password, userType=userType)
    user.save()
    user = get_user_by_email(email)
    if user["message"] == "success":
        return {
            "id": user["id"],
            "email": user["email"],
            "message": "User added successfully!",
        }
    return {"id": None, "email": None, "message": "An Error occurred!"}


def add_client(data):
    client = Client(**data)
    client.save()
    client = get_client_by_contract(data["contract"])
    if client["message"] == "success":
        return {
            "client": client,
            "message": "User added successfully!",
        }
    return {"client": None, "message": "An Error occurred!"}


def delete_client(contract):
    try:
        client = Client.objects.get(contract=contract)
        client.delete()
        return {"message": "Client deleted successfully!", "client": client}
    except Client.DoesNotExist:
        return {"message": "Client does not exist.", "client": None}


# def populate_clients():
#     directory = "./ports_updated"
#     file_names = []
#     ports = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             file_names.append(file)
#     for json_file in file_names:
#         with open(f"{directory}/{json_file}", "r") as f:
#             clients = json.loads(f.read())
#             for client in clients:
#                 full_name = client["name"].strip()
#                 full_name = re.sub(r"\.\d+", "", full_name)
#                 del client["pwr"]
#                 del client["name"]
#                 client["name_1"] = full_name.split(" ")[0]
#                 client["name_2"] = full_name.split(" ")[1]
#                 client["contract"] = full_name.split(" ")[2].zfill(10)
#                 client = Client(**client)
#                 client.save()
