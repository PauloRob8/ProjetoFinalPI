from django.shortcuts import redirect, render
from django.views.generic.base import View
from perfis.models import Perfil
from post.models import Post
# Create your views here.

class FazerPostView(View):
    template_name = 'pagina_inicial.html'

    def get(self, request):
        return redirect('pagina-inicial')
    
    def post(self, request):
        return redirect('pagina-inicial')