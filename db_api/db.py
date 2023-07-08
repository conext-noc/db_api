from django.contrib.auth.hashers import make_password
from db_api.models import User, Clients, Plans

lookup_types = ["S", "C", "D"]

port_lookup_types = ["DT", "CA", "VT", "VP"]


def client_to_dict(client):
    result = {
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
    return result


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


def get_client(lookup_type, lookup_value):
    if lookup_type not in lookup_types:
        return {"message": "bad type", "data": None, "error": True}

    try:
        if lookup_type == "S":
            client = Clients.objects.get(sn=lookup_value)
        if lookup_type == "C":
            client = Clients.objects.get(contract=lookup_value)
        if lookup_type == "D":
            client = Clients.objects.get(fspi=lookup_value)

        returned_client = client_to_dict(client)
        returned_client["srv_profile"] = returned_client["plan_name"].srv_profile
        returned_client["line_profile"] = returned_client["plan_name"].line_profile
        returned_client["plan_idx"] = returned_client["plan_name"].plan_idx
        returned_client["vlan"] = returned_client["plan_name"].vlan
        returned_client["plan_name"] = returned_client["plan_name"].plan_name
        return {"data": returned_client, "message": "success", "error": False}
    except Clients.DoesNotExist:
        return {"data": None, "message": "Client does not exist!", "error": True}


def get_clients(lookup_type, lookup_value):
    if lookup_type not in port_lookup_types:
        return {"message": "bad type", "clients": None, "error": True}

    if lookup_type == "DT":
        clients = (
            Clients.objects.filter(state="deactivated")
            .order_by("frame", "slot", "port", "onu_id")
            .values()
        )
    if lookup_type == "CA":
        clients = (
            Clients.objects.all().order_by("frame", "slot", "port", "onu_id").values()
        )
    if lookup_type == "VT":
        clients = (
            Clients.objects.all().order_by("frame", "slot", "port", "onu_id").values()
        )
    if lookup_type == "VP":
        clients = Clients.objects.filter(fsp=lookup_value).order_by("onu_id").values()

    return {"message": "success", "data": list(clients), "error": False}


def get_plans():
    plans = Plans.objects.all().values()
    # print(plans)
    return {"message": "success", "data": list(plans)}


def add_plan(plan_data):
    plan = Plans(**plan_data)
    plan.save()
    return {
        "plan": plan_data,
        "message": "Plan added successfully!",
    }


def update_plan():
    return


def delete_plan():
    return


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


def add_client(data):
    data["plan_name"] = Plans.objects.get(plan_name=data["plan_name"])
    client = Clients(**data)
    client.save()
    client = get_client("C", data["contract"])
    if client["message"] == "success":
        return {
            "data": client["data"],
            "message": "User added successfully!",
            "error": False,
        }
    return {"data": None, "message": "An Error occurred!", "error": True}


def delete_client(lookup_type, lookup_value):
    if lookup_type not in lookup_types:
        return {"message": "bad type", "data": None, "error": True}
    try:
        if lookup_type == "S":
            client = Clients.objects.get(sn=lookup_value)
        if lookup_type == "C":
            client = Clients.objects.get(contract=lookup_value)
        if lookup_type == "D":
            client = Clients.objects.get(fspi=lookup_value)

        returned_client = client_to_dict(client)
        returned_client["srv_profile"] = returned_client["plan_name"].srv_profile
        returned_client["line_profile"] = returned_client["plan_name"].line_profile
        returned_client["plan_idx"] = returned_client["plan_name"].plan_idx
        returned_client["vlan"] = returned_client["plan_name"].vlan
        returned_client["plan_name"] = returned_client["plan_name"].plan_name
        client.delete()
        return {
            "message": "Client deleted successfully!",
            "data": returned_client,
            "error": False,
        }
    except Clients.DoesNotExist:
        return {"message": "Client does not exist.", "data": None, "error": True}


def modify_client(lookup_type, lookup_value, change_field, new_values):
    fields = [
        "CO",
        "CT",
        "CP",
        "CV",
        "OX",
    ]
    if change_field not in fields or lookup_type not in lookup_types:
        return {"message": "bad type", "data": None, "error": True}

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
            client = Clients.objects.get(fspi=lookup_value)
            contract = client.contract

        if change_field == "CT":
            client.name_1 = new_values["name_1"]
            client.name_2 = new_values["name_2"]
            contract = new_values["contract"]

        elif change_field == "CO":
            client.sn = new_values["sn"]

        elif change_field == "CP":
            new_plan = Plans.objects.get(plan_name=new_values["plan_name"])
            client.plan_name = new_plan

        elif change_field == "OX":
            client.state = new_values["state"]

        client.save()
        client = Clients.objects.filter(contract=contract).values()[0]
        return {
            "message": "Client updated successfully!",
            "data": client,
            "error": False,
        }

    except Clients.DoesNotExist:
        return {"message": "Client does not exist.", "data": None, "error": True}


def populate(client_list):
    for client in client_list:
        print(client)
        client["plan_name"] = Plans.objects.get(plan_name=client["plan_name"])
        client_db = Clients(**client)
        client_db.save()
    return {"message": "Success!"}
