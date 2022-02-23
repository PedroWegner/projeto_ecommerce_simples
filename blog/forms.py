from django import forms
from django.contrib.auth.models import User
from . import models


class PostForms(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = '__all__'
        exclude = ('autor_post', 'data_post', 'publicado')


class ComentarioForms(forms.ModelForm):
    class Meta:
        model = models.Comentario
        fields = ('nome_comentario', 'email_comentario', 'comentario')
