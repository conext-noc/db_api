from django.contrib.auth.hashers import make_password
from db_api.models import User, Clients

lookup_types = ["S", "C", "D"]


def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        return {
            "id": user.id,
            "email": user.email,
            "password": user.password,
            "user_type": user.user_type,
            "message": "success",
        }
    except User.DoesNotExist:
        return {"id": None, "email": None, "message": "An Error occurred!"}


def get_client(lookup_type, lookup_value):
    if lookup_type not in lookup_types:
        return {"message": "bad type", "client": None}

    try:
        if lookup_type == "S":
            client = Clients.objects.get(sn=lookup_value)
        if lookup_type == "C":
            client = Clients.objects.get(contract=lookup_value)
        if lookup_type == "D":
            FRAME = lookup_value.split("/")[0]
            SLOT = lookup_value.split("/")[1]
            PORT = lookup_value.split("/")[2]
            ONU_ID = lookup_value.split("/")[3]
            client = Clients.objects.filter(fspi=f"{FRAME}/{SLOT}/{PORT}/{ONU_ID}")

        returned_client = {
            field: getattr(client, field)
            for field in [
                "frame",
                "slot",
                "port",
                "onu_id",
                "olt",
                "fsp",
                "fspi",
                "name_1",
                "name_2",
                "contract",
                "status",
                "state",
                "sn",
                "device",
                "plan_idx",
                "plan_name",
                "provider",
                "line_profile",
                "srv_profile",
                "gem_port",
                "spid",
            ]
        }
        return {
            "client": returned_client,
            "message": "success",
        }
    except Clients.DoesNotExist:
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
    client = Clients(**data)
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
            client = Clients.objects.get(sn=lookup_value)
        if lookup_type == "C":
            client = Clients.objects.get(contract=lookup_value)
        if lookup_type == "D":
            FRAME = lookup_value.split("/")[0]
            SLOT = lookup_value.split("/")[1]
            PORT = lookup_value.split("/")[2]
            ONU_ID = lookup_value.split("/")[3]
            client = Clients.objects.filter(fspi=f"{FRAME}/{SLOT}/{PORT}/{ONU_ID}")
        returned_client = {
            field: getattr(client, field)
            for field in [
                "frame",
                "slot",
                "port",
                "onu_id",
                "olt",
                "fsp",
                "fspi",
                "name_1",
                "name_2",
                "contract",
                "status",
                "state",
                "sn",
                "device",
                "plan_idx",
                "plan_name",
                "provider",
                "line_profile",
                "srv_profile",
                "gem_port",
                "spid",
            ]
        }
        client.delete()
        return {"message": "Client deleted successfully!", "client": returned_client}
    except Clients.DoesNotExist:
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

    contract = None
    client = None

    try:
        if lookup_type == "S":
            client = Clients.objects.get(sn=lookup_value)
            contract = client.contract
        if lookup_type == "C":
            client = Clients.objects.get(contract=lookup_value)
            contract = client.contract
        if lookup_type == "D":
            FRAME = lookup_value.split("/")[0]
            SLOT = lookup_value.split("/")[1]
            PORT = lookup_value.split("/")[2]
            ONU_ID = lookup_value.split("/")[3]
            client = Clients.objects.filter(fspi=f"{FRAME}/{SLOT}/{PORT}/{ONU_ID}")
            contract = client.contract

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
        client = Clients.objects.get(contract=contract)
        returned_client = {
            field: getattr(client, field)
            for field in [
                "frame",
                "slot",
                "port",
                "onu_id",
                "olt",
                "fsp",
                "fspi",
                "name_1",
                "name_2",
                "contract",
                "status",
                "state",
                "sn",
                "device",
                "plan_idx",
                "plan_name",
                "provider",
                "line_profile",
                "srv_profile",
                "gem_port",
                "spid",
            ]
        }
        return {"message": "Client updated successfully!", "client": returned_client}

    except Clients.DoesNotExist:
        return {"message": "Client does not exist.", "client": None}


def populate(client_list):
    for client in client_list:
        client["name_1"] = client["name"].split(" ")[0]
        client["name_2"] = client["name"].split(" ")[1]
        client["contract"] = client["name"].split(" ")[2].zfill(10)
        del client["name"]
        client_db = Clients(**client)
        client_db.save()
    return {"message": "Success!"}
