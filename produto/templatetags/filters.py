from django.template import Library
from utilidades import utilidades


register = Library()


@register.filter
def forma_preco(float):
    return utilidades.forma_preco(float)


@register.filter
def compra_total(carrinho):
    return utilidades.compra_total(carrinho)


@register.filter
def quantidade_total(carrinho):
    return utilidades.quantidade_total(carrinho)
