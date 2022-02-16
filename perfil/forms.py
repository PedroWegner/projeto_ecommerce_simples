from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForms(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario', )
