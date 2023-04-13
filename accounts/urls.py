from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path("cadaster/", views.cadaster, name="cadaster"),
    path("login/", views.login, name="login"),
]
