from django.shortcuts import redirect, render
from django.views.generic.base import View
from perfis.views import *
from perfis.models import Perfil
from django.contrib.auth.models import User
from post.models import Post
from post.forms import *
# Create your views here.

class FazerPostView(View):
    template_name = 'pagina_inicial.html'
    
    def get(self,request):
        return redirect('pagina-inicial')
    
    def post(self,request):
        form = FazerPostForm(request.POST)
        if form.is_valid():
            logado = get_perfil_logado(request)
            dados_form = form.cleaned_data
            texto = '' +dados_form['post']
            post = Post(conteudo = texto, autor = logado, amei = 0, odiei = 0, triste = 0, legal = 0)
            post.save()
        return redirect('pagina-inicial')

class EditarPostView(View):
    def get(self,request):
        return redirect('pagina-inicial')
    
    def post(self,request, post_id):
        form = FazerPostForm(request.POST)
        if form.is_valid():
            logado = get_perfil_logado(request)
            post = Post.objects.get(id = post_id)
            dados_form = form.cleaned_data
            texto = '' +dados_form['post']
            post.conteudo = texto
            post.save()
        return redirect('pagina-inicial')

class FazerComentarioView(View):
    def get(self,request):
        return redirect('pagina-inicial')
    
    def post(self,request, post_id):
        form = FazerPostForm(request.POST)
        logado = get_perfil_logado(request)
        postagem = Post.objects.get(id = post_id)
        if form.is_valid(): 
            dados_form = form.cleaned_data
            texto = '' +dados_form['post']
            comentario = Comentario(conteudo = texto, post = postagem, autor = logado)
            comentario.save()
        return redirect('pagina-inicial')

class FazerMarcacaoView(View):
    def get(self,request):
        return redirect('pagina-inicial')
    
    def post(self,request, post_id):
        form = FazerPostForm(request.POST)
        postagem = Post.objects.get(id = post_id)
          
        
        if form.is_valid():
            dados_form = form.cleaned_data
            nome_marcado = ''+dados_form['post']
            pode_marcar = Perfil.objects.filter(nome = nome_marcado).exists()
            if pode_marcar:
                para_marca = Perfil.objects.get(nome = nome_marcado)
                is_exist = Marcacoes.objects.filter(post = postagem.id, marcado = para_marca.id)

                if not is_exist:
                    marcacao = Marcacoes(post = postagem.id, marcado = para_marca.id)
                    marcacao.save()
                return redirect('pagina-inicial')
        
        return redirect('pagina-inicial')

@login_required
def excluir_postagem(request, post_id):
    logado = get_perfil_logado(request)
    post = Post.objects.get(id = post_id)
    user = logado.usuario
    is_super = user.is_superuser
    outher_user = post.autor.usuario.is_superuser
    
    if is_super:
        if not outher_user:
            post.delete()
            return redirect('pagina-inicial')
        elif post.autor == logado:
            post.delete()
            return redirect('pagina-inicial')
        else:
            return redirect('pagina-inicial')
    elif post.autor == logado:
            post.delete()
            return redirect('pagina-inicial')
    
    return redirect('pagina-inicial')

