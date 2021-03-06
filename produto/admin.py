from django.contrib import admin
from .models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'get_preco', 'estoque']


admin.site.register(Produto, ProdutoAdmin)
