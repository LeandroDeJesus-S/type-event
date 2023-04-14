from django.urls import path
from . import views


app_name = 'events'
urlpatterns = [
    path('novo-evento/', views.new_events, name='new_event'),
    path('gerenciar-eventos/', views.manage_event, name='manage_event'),
    path('inscrever-se/<int:event_id>/', views.subscribe_event, name='inscrever_evento'),
    path('participantes-evento/<int:event_id>/', views.participants_event, name='participantes_evento'),
    path('gerar_csv/<int:id>/', views.generate_csv, name="gerar_csv"),
    path('certificados/<int:id>/', views.certificates, name="certificados_evento"),
    path('gerar-certificado/<int:id>/', views.generate_certificate, name="gerar_certificado"),
]
