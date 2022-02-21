from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.CadastraPerfil.as_view(), name='cadastrar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
