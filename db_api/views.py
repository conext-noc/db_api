import os
from rest_framework.response import Response
from rest_framework import generics
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from dotenv import load_dotenv
from db_api.db import (
    get_user_by_email,
    add_user,
    add_client,
    get_client_by_contract,
    delete_client,
)
from db_api.jwt_utils import generate_token

load_dotenv()


class DbApi(generics.GenericAPIView):
    def get(self, _):
        return HttpResponse("ms_running", status=200)


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
                "exp_time": exp_time,
                "email": res["email"],
                "userType": res["userType"],
            },
            status=200,
        )


class AddUser(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = add_user(data["email"], data["password"], data["userType"])
        if res["id"] is None:
            return Response(res, status=500)
        return Response(res, status=200)


class MsHealthCheck(generics.GenericAPIView):
    def get(self, _):
        # if req.META["HTTP_CONEXT_KEY"] == os.environ["CONEXT_KEY"]:
        # data = request.data
        # if data["API_KEY"] != os.environ["API_KEY"]:
        #     return HttpResponse("Unauthorized", status=401)
        # res = add_user(data["email"], data["password"], data["userType"])
        return Response({"message": "ok"}, status=200)


class Client(generics.GenericAPIView):
    def get(self, request):
        if request.META["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        contract = request.query_params.get("contract")
        res = get_client_by_contract(contract)
        if res["client"] is None:
            return Response(res, status=500)
        return Response(res, status=200)

    def post(self, request):
        data = request.data
        if (
            data["API_KEY"] != os.environ["API_KEY"]
            and request.META["API_KEY"] != os.environ["API_KEY"]
        ):
            return HttpResponse("Unauthorized", status=401)
        client = data["client"]
        full_name = client["name"].strip()
        del client["pwr"]
        del client["name"]
        client["name_1"] = full_name.strip().split(" ")[0]
        client["name_2"] = full_name.strip().split(" ")[1]
        client["contract"] = full_name.strip().split(" ")[2].zfill(10)
        res = add_client(client)
        if res["client"] is None:
            return Response(res, status=500)
        return Response(res, status=200)

    def delete(self, request):
        if request.META["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        contract = request.query_params.get("contract")
        res = delete_client(contract)
        if res["client"] is None:
            return Response(res, status=500)
        return Response(res, status=200)

    # add patch method to update the given client
    # once finished this method finish up the mod ms
    # then update th oltOperations to work with this db
