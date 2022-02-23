from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.categoria


class Post(models.Model):
    titulo_post = models.CharField(max_length=50, verbose_name='Título')
    categoria_post = models.ForeignKey(
        Categoria, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='Categoria')
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    conteudo_post = models.TextField(verbose_name='Conteúdo')
    data_post = models.DateField(default=timezone.now)
    imagem_post = models.ImageField(
        upload_to='imagens_blog/%Y/%m', null=True, blank=True)
    publicado = models.BooleanField(default=False, verbose_name="Visibildiade")

    def __str__(self):
        return self.titulo_post


class Comentario(models.Model):
    nome_comentario = models.CharField(max_length=50)
    email_comentario = models.EmailField()
    comentario = models.TextField(verbose_name='Comentário')
    post_comentario = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario_comentario = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True)
    data_comentario = models.DateField(default=timezone.now)
    publicado_comentario = models.BooleanField(default=False)

    def __str__(self):
        return f'Comentário de {self.nome_comentario}'
