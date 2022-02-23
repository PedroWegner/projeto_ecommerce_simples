from django import forms
from django.contrib.auth.models import User
from . import models


class ProdutoCadastroForms(forms.ModelForm):
    class Meta:
        model = models.Produto
        fields = '__all__'
        exclude = ('slug',)
