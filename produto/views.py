import imp
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AddCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )

        variacao_id = self.request.GET.get('vid')
