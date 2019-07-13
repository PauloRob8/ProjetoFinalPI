from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic.base import View
from perfis.models import Perfil
from perfis.views import exibir_perfil
from usuarios.forms import *

# Create your views here.

class RegistrarUsuarioView(View):
    template_name = 'registrar.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username = dados_form['nome'],email = dados_form['email'],password = dados_form ['senha'])

            perfil = Perfil(nome=dados_form['nome'],telefone=dados_form['telefone'],nome_empresa=dados_form['nome_empresa'],
                usuario=usuario)

            perfil.save()
            return redirect('pagina-inicial')
        return render(request, self.template_name, {'form' : form})

class MudarSenhaView(View):
    template_name = 'mudar-senha.html'

    
    def get(self, request, perfil_id):
        return redirect('index')

    def post(self, request, perfil_id):
        form = MudarSenhaForm(request.POST)
        logado = Perfil.objects.get(id = perfil_id)

        if form.is_valid():
            dados_form = form.cleaned_data

            if dados_form['senha_nova'] == dados_form['senha_confirmacao']:
                logado = Perfil.objects.get(id = perfil_id)
                user_id = logado.usuario.id
                user = User.objects.get(id = user_id)
                is_my_pass = user.check_password(dados_form['senha_atual'])

                if is_my_pass:
                    user.set_password(dados_form['senha_nova'])
                    user.save()
                    return render(request, 'perfil.html',{'perfil' : logado, 'perfil_logado' : logado,'is_me' : True})
                else:
                    form.adiciona_erro("Senha Atual incorreta")
            else:
                form.adiciona_erro("Senha nova e confirmação não batem")
        
        return render(request, self.template_name, {'form' : form,'perfil_logado' : logado, 'perfil_id' : perfil_id})

        
        
        