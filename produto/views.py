import imp
from django import http
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
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
        """
        if self.request.session.get('carrinho'):
            del self.request.session['carrinho']
            self.request.session.save()
        """

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista_produtos')
        )

        id_produto = self.request.GET.get('id')

        produto = get_object_or_404(
            models.Produto, id=id_produto
        )

        estoque_produto = produto.estoque
        nome_produto = produto.nome
        nome_cient_produto = produto.nome_cientifico
        preco_produto = produto.preco
        slug_produto = produto.slug
        imagem_produto = produto.imagem

        if imagem_produto:
            imagem_produto = imagem_produto.name
        else:
            imagem_produto = ''

        if produto.estoque < 1:
            messages.error(
                self.request,
                'Não há estoque'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if id_produto in carrinho:
            quantidade_carrinho = carrinho[id_produto]['quantidade']
            quantidade_carrinho += 1
            if estoque_produto < quantidade_carrinho:

                messages.warning(
                    self.request,
                    'Estoque insuficiente.'
                )

                quantidade_carrinho = estoque_produto

            carrinho[id_produto]['quantidade'] = quantidade_carrinho
            carrinho[id_produto]['preco_produto'] = preco_produto * \
                quantidade_carrinho

        else:
            carrinho[id_produto] = {
                'id_produto': id_produto,
                'nome_produto': nome_produto,
                'nome_cient_produto': nome_cient_produto,
                'preco_produto': preco_produto,
                'quantidade': 1,
                'slug_produto': slug_produto,
                'imagem_produto': imagem_produto,

            }

        self.request.session.save()

        messages.success(
            self.request,
            'Produto adicionado ao carrinho'
        )
        return redirect(http_referer)


class RemoveCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista_produtos')
        )

        id_produto = self.request.GET.get('id')

        if not id_produto:
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if id_produto not in self.request.session['carrinho']:
            return redirect(http_referer)

        messages.success(
            self.request,
            'O produto foi removido do carrinho'
        )

        del self.request.session['carrinho'][id_produto]
        self.request.session.save()
        return redirect(http_referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        context = {
            'carrinho': self.request.session.get('carrinho')
        }

        return render(self.request, 'produto/carrinho.html', context)
