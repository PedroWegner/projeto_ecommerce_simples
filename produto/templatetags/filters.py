from django.template import Library
from utilidades import utilidades


register = Library()


@register.filter
def forma_preco(float):
    return utilidades.forma_preco(float)
