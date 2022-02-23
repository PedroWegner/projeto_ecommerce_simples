from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Blog.as_view(), name='blog'),
    path('publicar', views.PublicaPost.as_view(), name='publicar'),
    path('post/<int:pk>', views.PostDetalheDois.as_view(), name='post_detalhe'),
]
