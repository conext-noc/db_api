from django.urls import path
from db_api.views import DbApi, SignIn, AddUser, MsHealthCheck, Client

urlpatterns = [
    path("", DbApi.as_view()),
    path("signin", SignIn.as_view()),
    path("adduser", AddUser.as_view()),
    path("client", Client.as_view()),
    path("ms-health-check", MsHealthCheck.as_view()),
    # path("populate", AddAllClients.as_view()),
]
