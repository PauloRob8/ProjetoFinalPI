from django.shortcuts import redirect, render
from django.views.generic.base import View
from perfis.views import *
from perfis.models import Perfil
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
        return pagina_inicial(request)


