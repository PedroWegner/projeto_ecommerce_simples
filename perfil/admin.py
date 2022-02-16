from django.contrib import admin
from .models import Endereco, Perfil


class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'endereco']


class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['rua', 'numero', 'bairro', 'cep']


admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Endereco, EnderecoAdmin)