from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    quantidade_total = models.PositiveIntegerField()
    status = models.CharField(
        default='A',
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pedente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )

    def __str__(self):
        return f'Pedido N. {self.id}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=200)
    produto_id = models.PositiveIntegerField()
    preco = models.FloatField()
    quantidade = models.PositiveIntegerField()
    imagem = models.ImageField()

    def __str__(self):
        return f'Item do {self.pedido}'

    class Meta():
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
