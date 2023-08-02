from db_api.models import Alarms, Clients


# CREATE
def add_alarms(data):
    alarms = data["alarms"]
    for alarm in alarms:
        alarm["contract"] = Clients.objects.get(contract=alarm["contract"])
        alarms_db = Alarms(**alarm)
        alarms_db.save()

    return {"message": "Success!", "error": False}


# READ
def get_alarms():
    alarms = Alarms.objects.all().values()
    return {"message": "Success!", "error": False, "data": list(alarms)}


# UPDATE - DELETE
def empty_alarms():
    Alarms.objects.all().delete()
    return {"message": "Success!", "error": False}
