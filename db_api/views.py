import os
from rest_framework.response import Response
from rest_framework import generics
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from dotenv import load_dotenv
from db_api.db import get_user_by_email, add_user

load_dotenv()


class DbApi(generics.GenericAPIView):
    def get(self):
        status_code = 200
        response_text = "ms_running"
        return HttpResponse(response_text, status=status_code)


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
        return Response(
            {
                "message": "Signed In",
                "User": data,
            },
            status=200,
        )


class AddUser(generics.GenericAPIView):
    def post(self, request):
        data = request.data
        if data["API_KEY"] != os.environ["API_KEY"]:
            return HttpResponse("Unauthorized", status=401)
        res = add_user(data["email"], data["password"])
        if res["id"] is None:
            return Response(res, status=500)
        return Response(res, status=200)
