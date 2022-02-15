from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from . import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
