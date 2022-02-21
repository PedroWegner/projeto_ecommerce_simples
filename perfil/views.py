import copy
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from . import forms
from django.contrib import messages


class CadastraPerfil(View):
    template_name = 'perfil/cadastra.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'perfilforms': forms.PerfilForms(
                data=self.request.POST or None,
            ),
            'userform': forms.UsuarioForms(
                data=self.request.POST or None,
            ),
            'enderecoforms': forms.EnderecoForms(
                data=self.request.POST or None,
            ),
        }

        self.perfilforms = self.contexto['perfilforms']
        self.enderecoforms = self.contexto['enderecoforms']
        self.userform = self.contexto['userform']

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        # indica que há algum erro num dos formularios
        if not self.userform.is_valid() or not self.enderecoforms.is_valid() or not self.perfilforms.is_valid():
            return self.renderizar

        senha = self.userform.cleaned_data.get('senha')

        # registra um usuario
        usuario = self.userform.save(commit=False)
        usuario.set_password(senha)
        usuario.save()

        # registra um endereco
        endereco = self.enderecoforms.save(commit=False)
        endereco.save()

        # registra um perfil
        perfil = self.perfilforms.save(commit=False)
        perfil.usuario = usuario
        perfil.endereco = endereco
        perfil.save()

        self.request.session.save()
        return self.renderizar


class Login(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'perfil/login.html')

    def post(self, *args, **kwargs):
        usuario = self.request.POST.get('usuario')
        senha = self.request.POST.get('senha')

        if not usuario or not senha:
            messages.error(
                self.request,
                'Usuario ou senha inválidos'
            )

        usuario = authenticate(self.request, username=usuario, password=senha)

        if usuario:
            login(self.request, user=usuario)

        return redirect('produto:carrinho')


class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))
        logout(self.request)
        self.request.session['carrinho'] = carrinho
        return redirect('produto:lista_produtos')
