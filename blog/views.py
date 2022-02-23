from multiprocessing import context
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView
from .forms import ComentarioForms, PostForms
from .models import Comentario, Post
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView


class Blog(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'


class PublicaPost(View):
    template_name = 'blog/publicar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'postforms': PostForms(
                data=self.request.POST or None,
            ),
        }

        self.postforms = self.contexto['postforms']

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            redirect('produto:lista_produtos')

        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.postforms.is_valid():
            return self.renderizar

        # registra um post
        post = self.postforms.save(commit=False)
        post.autor_post = self.request.user
        post.save()

        self.request.session.save()
        return self.renderizar


class PostDetalhe(View):
    template_name = 'post/postdetalhes.html'
    model = Post
    form_class = ComentarioForms
    context_object_name = 'post'

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(
            publicado_comentario=True,
            post_comentario=post.id
        )
        contexto['comentarios'] = comentarios

    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.post_comentario = post

        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user

        comentario.save()
        messages.success(
            self.request,
            'Comentário enviado'
        )

        return redirect('blog:post_detalhes', pk=post.id)


class PostDetalheDois(DetailView):
    template_name = 'blog/detalhepost.html'
    model = Post
    pk_url_kwarg = 'pk'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'comentarioforms': ComentarioForms(
                data=self.request.POST or None,
            ),
            'post': self.get_object(),
        }

        self.comentarioforms = self.contexto['comentarioforms']
        self.post_obj = self.contexto['post']
        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):

        comentario = self.comentarioforms.save(commit=False)
        # checa se ha usuario logado
        comentario.post_comentario = self.post_obj
        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user
        comentario.save()

        return redirect('blog:post_detalhe', pk=self.post_obj.id)
