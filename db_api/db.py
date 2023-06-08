from django.contrib.auth.hashers import make_password
from django.db.models import Q
from db_api.models import User, Client

lookup_types = ["S", "N", "D"]


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


def get_client(lookup_type, lookup_value):
    if lookup_type not in lookup_types:
        return {"message": "bad type", "client": None}

    try:
        if lookup_type == "S":
            client = Client.objects.get(sn=lookup_value)
        if lookup_type == "N":
            client = Client.objects.get(contract=lookup_value)
        if lookup_type == "D":
            FRAME = lookup_value.split("/")[0]
            SLOT = lookup_value.split("/")[1]
            PORT = lookup_value.split("/")[2]
            ONU_ID = lookup_value.split("/")[3]
            print(FRAME, SLOT, PORT, ONU_ID)
            client = Client.objects.filter(
                Q(fsp=f"{FRAME}/{SLOT}/{PORT}") & Q(onu_id=ONU_ID)
            )
            print(client)

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
        return {"client": None, "message": "Client does not exist!"}


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
    client = get_client("N", data["contract"])
    if client["message"] == "success":
        return {
            "client": client,
            "message": "User added successfully!",
        }
    return {"client": None, "message": "An Error occurred!"}


def delete_client(lookup_type, lookup_value):
    if lookup_type not in lookup_types:
        return {"message": "bad type", "client": None}

    try:
        if lookup_type == "S":
            client = Client.objects.get(sn=lookup_value)
        if lookup_type == "N":
            client = Client.objects.get(contract=lookup_value)
        if lookup_type == "D":
            client = Client.objects.get(fsp=lookup_value)
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
        client.delete()
        return {"message": "Client deleted successfully!", "client": returned_client}
    except Client.DoesNotExist:
        return {"message": "Client does not exist.", "client": None}


def modify_client(lookup_type, lookup_value, change_field, new_values):
    fields = [
        "CO",
        "CT",
        "CP",
        "CV",
        "OX",
    ]
    if change_field not in fields or lookup_type not in lookup_types:
        return {"message": "bad type", "client": None}

    try:
        if lookup_type == "S":
            client = Client.objects.get(sn=lookup_value)
        if lookup_type == "N":
            client = Client.objects.get(contract=lookup_value)
        if lookup_type == "D":
            client = Client.objects.get(fsp=lookup_value)

        if change_field == "CT":
            client.name_1 = new_values["name_1"]
            client.name_2 = new_values["name_2"]
            client.contract = new_values["contract"]
            contract = new_values["contract"]

        elif change_field == "CO":
            client.sn = new_values["sn"]

        elif change_field == "CP":
            client.plan = new_values["plan"][:-2]
            client.vlan = new_values["provider"]

        elif change_field == "OX":
            client.state = new_values["state"]

        client.save()
        client = Client.objects.get(contract=contract)
        return {"message": "Client updated successfully!", "client": client}

    except Client.DoesNotExist:
        return {"message": "Client does not exist.", "client": None}
