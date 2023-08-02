from db_api.models import Ports


# CREATE
def add_ports(data):
    ports = data["ports"]
    for port in ports:
        print(port)
        ports_db = Ports(**port)
        ports_db.save()
    return {"message": "successfully added ports", "error": False}


# READ
def get_ports():
    ports = Ports.objects.all().values()
    return {"message": "success", "error": False, "ports": list(ports)}


# UPDATE
def open_port(data):
    port = data["port"]
    olt = data["olt"]
    fspo = f"{port}-{olt}"
    port_db = Ports.objects.get(fspo=fspo)
    port_db.is_open = True
    port_db.save()
    return {"message": "successfully opened port", "error": False}


# DISABLE/Delete
def disable_port(data):
    port = data["port"]
    olt = data["olt"]
    fspo = f"{port}-{olt}"
    port_db = Ports.objects.get(fspo=fspo)
    port_db.is_open = False
    port_db.save()
    return {"message": "successfully closed port", "error": False}
