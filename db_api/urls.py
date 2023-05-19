from django.urls import path
from .views import DbApi

urlpatterns = [path("", DbApi.as_view())]
