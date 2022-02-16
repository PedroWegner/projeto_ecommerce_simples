from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForms(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario', 'endereco',)


class EnderecoForms(forms.ModelForm):
    class Meta:
        model = models.Endereco
        fields = '__all__'


class UsuarioForms(forms.ModelForm):
    senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )
    senha_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação da senha',
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'senha', 'senha_confirm')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        senha_data = cleaned.get('senha')
        senha_confirm_data = cleaned.get('senha_confirm')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()
