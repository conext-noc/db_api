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

# UPDATE
def update_alarm(data):
    alarms = data["alarms"]
    for alarm in alarms:
        old_alarm = Alarms.objects.get(contract=alarm["contract"])
        old_alarm.last_down_time = alarm["last_down_time"]
        old_alarm.last_down_date = alarm["last_down_date"]
        old_alarm.save()

    return {"message": "Success!", "error": False}

# UPDATE
def remove_alarm(data):
    alarms = data["alarms"]
    for alarm in alarms:
        old_alarm = Alarms.objects.get(contract=alarm["contract"])
        old_alarm.delete()

    return {"message": "Success!", "error": False}



# DELETE ALL
def empty_alarms():
    Alarms.objects.all().delete()
    return {"message": "Success!", "error": False}
