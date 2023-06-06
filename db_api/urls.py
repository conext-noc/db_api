from django.urls import path
from db_api.views import (
    DbApi,
    SignIn,
    AddUser,
    MsHealthCheck,
    GetClient,
    AddClient,
    UpdateClient,
    RemoveClient,
)

urlpatterns = [
    path("", DbApi.as_view()),
    path("signin", SignIn.as_view()),
    path("adduser", AddUser.as_view()),
    path("add-client", AddClient.as_view()),
    path("get-client", GetClient.as_view()),
    path("update-client", UpdateClient.as_view()),
    path("remove-client", RemoveClient.as_view()),
    path("ms-health-check", MsHealthCheck.as_view()),
    # path("populate", AddAllClients.as_view()),
]
