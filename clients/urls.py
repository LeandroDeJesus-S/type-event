from django.urls import path

from . import views

app_name = 'clients'
urlpatterns = [
    path("meus-certificados/", views.my_certificates, name="meus_certificados"),
    path("meus-eventos/", views.my_events, name="meus_eventos"),
    path("evento/<int:pk>", views.event, name="evento"),
]
