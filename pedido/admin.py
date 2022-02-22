from django.contrib import admin
from .models import Pedido, ItemPedido
# Register your models here.


class ItemPedidoInLine(admin.TabularInline):
    model = ItemPedido
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInLine
    ]


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
