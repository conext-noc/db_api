from django.urls import path
from db_api.views import DbApi, SignIn, AddUser

urlpatterns = [
    path("", DbApi.as_view()),
    path("signin", SignIn.as_view()),
    path("adduser", AddUser.as_view()),
]
