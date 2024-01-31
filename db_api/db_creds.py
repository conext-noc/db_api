from db_api.models import OltPasswords,SnmpPasswords


# # CREATE
# def add_creds(data):
#     creds = data["creds"]
#     creds_db = OltPasswords(**creds)
#     creds_db.save()
#     return {"message": "Success!", "error": False}


# READ
def get_creds():
    creds = OltPasswords.objects.all().values()
    return {"message": "Success!", "error": False, "data": list(creds)}

# READ
def get_community():
    creds = SnmpPasswords.objects.all().values()
    return {"message": "Success!", "error": False, "data": list(creds)}


# UPDATE - DELETE
# def empty_alarms():
#     Alarms.objects.all().delete()
#     return {"message": "Success!", "error": False}
