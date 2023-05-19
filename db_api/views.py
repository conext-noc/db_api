# import os
from rest_framework.response import Response
from rest_framework import generics
from django.http import HttpResponse
from dotenv import load_dotenv

load_dotenv()


class DbApi(generics.GenericAPIView):
    def get(self):
        status_code = 200
        response_text = "ms_running"
        return HttpResponse(response_text, status=status_code)

    def post(self, req):
        status_code = 200
        data = req.data
        # res = []
        return Response({"message": "OK", "data": data}, status_code=status_code)
        # else:
        #   return HttpResponse("Bad Request to server", status=400)
