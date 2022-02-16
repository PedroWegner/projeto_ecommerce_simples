from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.models import User
from . import forms


class CadastraPerfil(View):
    template_name = 'perfil/cadastra.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'userform': forms.PerfilForms(
                data=self.request.POST or None,
                usuario=self.request.user,
            )
        }
