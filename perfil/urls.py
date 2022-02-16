from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.CadastraPerfil.as_view(), name='cadastrar')
]
