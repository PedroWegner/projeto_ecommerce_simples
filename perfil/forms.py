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
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        senha_data = cleaned.get('senha')
        senha_confirm_data = cleaned.get('senha_confirm')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As duas senhas não conferem'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório.'

        if usuario_db:
            validation_error_msgs['username'] = error_msg_user_exists

        if email_db:
            validation_error_msgs['email'] = error_msg_email_exists

        if not senha_data:
            validation_error_msgs['senha'] = error_msg_required_field

        if not senha_confirm_data:
            validation_error_msgs['senha_confirm'] = error_msg_required_field

        if senha_data != senha_confirm_data:
            validation_error_msgs['senha'] = error_msg_password_match
            validation_error_msgs['senha_confirm'] = error_msg_password_match

        if len(senha_data) < 6:
            validation_error_msgs['senha'] = error_msg_password_short

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))
