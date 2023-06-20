from django.contrib.auth.hashers import make_password
from db_api.models import User, Clients, Plans

lookup_types = ["S", "C", "D"]

port_lookup_types = ["DT", "CA", "VT", "VP"]


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
                "contract",
                "frame",
                "slot",
                "port",
                "onu_id",
                "olt",
                "fsp",
                "fspi",
                "name_1",
                "name_2",
                "status",
                "state",
                "sn",
                "device",
                "plan_name",
                "spid",
            ]
        }
        returned_client["srv_profile"] = returned_client["plan_name"].srv_profile
        returned_client["line_profile"] = returned_client["plan_name"].line_profile
        returned_client["plan_idx"] = returned_client["plan_name"].plan_idx
        returned_client["vlan"] = returned_client["plan_name"].vlan
        returned_client["plan_name"] = returned_client["plan_name"].plan_name
        return {
            "client": returned_client,
            "message": "success",
        }
    except Clients.DoesNotExist:
        return {"client": None, "message": "Client does not exist!"}


def get_clients(lookup_type, lookup_value):
    if lookup_type not in port_lookup_types:
        return {"message": "bad type", "clients": None}

    if lookup_type == "DT":
        clients = Clients.objects.filter(state="deactivated").values()
    if lookup_type == "CA":
        clients = Clients.objects.all().values()
    if lookup_type == "VT":
        clients = Clients.objects.all().values()
    if lookup_type == "VP":
        FRAME = lookup_value.split("/")[0]
        SLOT = lookup_value.split("/")[1]
        PORT = lookup_value.split("/")[2]
        clients = Clients.objects.filter(fsp=f"{FRAME}/{SLOT}/{PORT}").values()

    return {"message": "success", "client": list(clients)}


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
                "contract",
                "frame",
                "slot",
                "port",
                "onu_id",
                "olt",
                "fsp",
                "fspi",
                "name_1",
                "name_2",
                "status",
                "state",
                "sn",
                "device",
                "plan_name",
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
                "contract",
                "frame",
                "slot",
                "port",
                "onu_id",
                "olt",
                "fsp",
                "fspi",
                "name_1",
                "name_2",
                "status",
                "state",
                "sn",
                "device",
                "plan_name",
                "spid",
            ]
        }
        return {"message": "Client updated successfully!", "client": returned_client}

    except Clients.DoesNotExist:
        return {"message": "Client does not exist.", "client": None}


def populate(client_list):
    for client in client_list:
        print(client)
        client["plan_name"] = Plans.objects.get(plan_name=client["plan_name"])
        client["name_1"] = client["name"].split(" ")[0]
        client["name_2"] = client["name"].split(" ")[1]
        client["contract"] = client["name"].split(" ")[2].zfill(10)
        del client["name"]
        client_db = Clients(**client)
        client_db.save()
    return {"message": "Success!"}
