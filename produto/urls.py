from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista_produtos'),
    path('<slug>', views.DetalheProduto.as_view(), name='detalhe_produto'),
    path('addcarrinho/', views.AddCarrinho.as_view(), name='add_carrinho'),
    path('removecarrinho/', views.RemoveCarrinho.as_view(), name='remove_carrinho'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name='resumo_da_compra'),

]
