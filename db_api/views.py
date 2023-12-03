import os
from rest_framework.response import Response
from rest_framework import generics
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from dotenv import load_dotenv
from db_api.db_alarms import get_alarms, add_alarms, empty_alarms
from db_api.db_plans import get_plans
from db_api.db_users import add_user, get_user_by_email, update_user
from db_api.db_ports import get_ports, add_ports, disable_port, open_port
from db_api.db_clients import (
    get_client,
    get_clients,
    delete_client,
    modify_client,
    add_client,
    populate,
)
from db_api.jwt_utils import generate_token
from db_api.ms_health_status import get_health_status
from db_api.db_creds import get_creds
from db_api.db_acl_rules import get_rules, add_rules, update_rules_ip

load_dotenv()


class DbApi(generics.GenericAPIView):
    def get(self, _):
        return HttpResponse("ms_running", status=200)


# --------------------------------------- USERS ---------------------------------------
class SignIn(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized?", status=401)
        res = get_user_by_email(data["email"])
        if check_password(res["password"], data["password"]):
            return Response(
                {
                    "message": "Bad Credentials",
                    "User": None,
                },
                status=401,
            )
        (token, exp_time) = generate_token(data["email"])
        return Response(
            {
                "message": "Signed In",
                "token": token,
                "expTime": exp_time,
                "email": res["email"],
                "userType": res["user_type"],
            },
            status=200,
        )


class AddUser(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = add_user(data["email"], data["password"], data["user_type"])
        if res["id"] is None:
            return Response(res, status=500)
        return Response(res, status=200)
    
    
class UpdateUser(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = update_user(data)
        if res["error"]:
            return Response(res, status=400)
        return Response(res, status=200)

# --------------------------------------- MS HEALTH CHECK ---------------------------------------
class MsHealthCheck(generics.GenericAPIView):
    def post(self, req):
        data = req.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = get_health_status()
        return Response(res, status=200)


# --------------------------------------- CLIENTS ---------------------------------------
class GetClient(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        lookup_type = data["lookup_type"]
        lookup_value = data["lookup_value"]
        res = get_client(lookup_type, lookup_value)
        return Response(res, status=200)


class GetClients(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        lookup_type = data["lookup_type"]
        lookup_value = data["lookup_value"]
        res = get_clients(lookup_type, lookup_value)
        return Response(res, status=200)


class AddClient(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        client = data["data"]
        res = add_client(client)
        return Response(res, status=200)


class RemoveClient(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        lookup_type = data["lookup_type"]
        lookup_value = data["lookup_value"]
        res = delete_client(lookup_type, lookup_value)
        return Response(res, status=200)


class UpdateClient(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if request.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        lookup_type = data["lookup_type"]
        lookup_value = data["lookup_value"]
        new_values = data["new_values"]
        change_field = data["change_field"]
        res = modify_client(lookup_type, lookup_value, change_field, new_values)
        return Response(res, status=200)


class PopulateDB(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if request.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = populate(data["client_list"])
        return Response(res, status=200)


# --------------------------------------- PLANS ---------------------------------------
class GetPlans(generics.GenericAPIView):
    def post(self, request):
        if request.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = get_plans()
        return Response(res, status=200)


# --------------------------------------- ALARMS ---------------------------------------
class GetAlarms(generics.GenericAPIView):
    def post(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = get_alarms()
        return Response(res, status=200)


class AddAlarms(generics.GenericAPIView):
    def post(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = add_alarms(req.data)
        return Response(res, status=200)


class EmptyAlarms(generics.GenericAPIView):
    def post(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = empty_alarms()
        return Response(res, status=200)


# --------------------------------------- PORTS ---------------------------------------
class GetPorts(generics.GenericAPIView):
    def post(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = get_ports()
        return Response(res, status=200)


class AddPorts(generics.GenericAPIView):
    def post(self, req):
        data = req.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = add_ports(req["data"])
        return Response(res, status=200)


class DisablePorts(generics.GenericAPIView):
    def post(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = disable_port(req.data)
        return Response(res, status=200)


class OpenPorts(generics.GenericAPIView):
    def post(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = open_port(req.data)
        return Response(res, status=200)


# --------------------------------------- CREDS ---------------------------------------
class Creds(generics.GenericAPIView):
    def post(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = get_creds()
        return Response(res, status=200)

# --------------------------------------- ACLS ----------------------------------------

class GetACLS(generics.GenericAPIView):
    def post(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = get_rules()
        return Response(res, status=200)

class CreateACLS(generics.GenericAPIView):
    def post(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = add_rules(req.data['acl_rules'])
        return Response(res, status=200)
    
class UpdateACLS(generics.GenericAPIView):
    def put(self, req):
        if req.data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = update_rules_ip(req.data['acl_rules'])
        return Response(res, status=200)