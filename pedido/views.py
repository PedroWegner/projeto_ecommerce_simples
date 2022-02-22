import imp
from re import template
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from utilidades import utilidades
from .models import Pedido, ItemPedido
import copy
from produto.models import Produto


class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            redirect('perfil:cadastrar')
        return super().dispatch(*args, **kwargs)


class Pagar(DispatchLoginRequired, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    # impedirah um usuario acessar pedidos que nao sejam dele
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa estar logado'
            )
            return redirect('perfil:cadastrar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Não há carrinho'
            )
            return redirect('produto:lista_produtos')

        carrinho = self.request.session.get('carrinho')
        carrinho_id_produto = [produto for produto in carrinho]

        bd_produto = list(
            Produto.objects.filter(
                id__in=carrinho_id_produto
            )
        )

        for produto in bd_produto:
            id_produto = str(produto.id)
            estoque = produto.estoque
            qtd_carrinho = carrinho[id_produto]['quantidade']
            preco_produto = carrinho[id_produto]['preco_produto']

            mensagem_erro = ''

            if estoque < qtd_carrinho:
                carrinho[id_produto]['quantidade'] = estoque
                carrinho[id_produto]['preco_produto'] = estoque * preco_produto
                mensagem_erro = 'Alguns produtos não tem estoque suficiente'

            if mensagem_erro:
                messages.error(
                    self.request,
                    mensagem_erro
                )

                self.request.session.save()
                return redirect('pedido:lista')

        quantidade_total = utilidades.quantidade_total(carrinho)
        valor_total = utilidades.compra_total(carrinho)

        pedido = Pedido(
            user=self.request.user,
            total=valor_total,
            quantidade_total=quantidade_total,
            status='C'
        )
        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=produto['nome_produto'],
                    produto_id=produto['id_produto'],
                    preco=produto['preco_produto'],
                    quantidade=produto['quantidade'],
                    imagem=produto['imagem_produto'],
                ) for produto in carrinho.values()
            ]
        )

        del self.request.session['carrinho']
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )


class Lista(View):
    def get(self, *args, **kwargs):
        pass


class Detalhe(View):
    pass
