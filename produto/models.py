from email.policy import default
from pickletools import optimize
from turtle import update
from django.conf import settings
from django.db import models
from utilidades import utilidades
from django.conf import settings
from django.utils.text import slugify
from PIL import Image
import os


class Produto(models.Model):
    nome = models.CharField(max_length=30)
    nome_cientifico = models.CharField(max_length=30)
    descricao_curta = models.TextField(max_length=250)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='imagens/%Y/%m')
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco = models.FloatField()
    estoque = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.nome

    def get_preco(self):
        return utilidades.forma_preco(self.preco)
    get_preco.short_description = 'Preço'

    @staticmethod
    def redimensiona_imagem(imagem, nova_largura=800):
        caminho_img = os.path.join(settings.MEDIA_ROOT, imagem.name)
        pillow_img = Image.open(caminho_img)
        largura_original, altura_original = pillow_img.size

        if largura_original >= nova_largura:
            return

        nova_altura = round(nova_largura * altura_original) / largura_original
        nova_img = pillow_img.resize(
            (nova_largura, nova_altura), Image.LANCZOS)
        nova_img.save(
            caminho_img,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            # TESTAR ESSA PK E ID
            self.ide = self.pk or self.id
            slug = f'{slugify(self.nome)}-{self.ide}-{slugify(self.nome_cientifico)}'
            self.slug = slug

        super().save(*args, **kwargs)
        tamanho_max = 200

        if self.imagem:
            self.redimensiona_imagem(self.imagem, tamanho_max)
