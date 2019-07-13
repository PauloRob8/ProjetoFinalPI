from django.shortcuts import render
from perfis.models import Perfil, Convite
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib.auth.models import User
# Create your views here.


def decidir_acao(request):
	exist =  User.objects.filter(username = 'carinha que mora logo ali').exists()
	if not exist:
		user_super = User.objects.create_user(username = 'carinha que mora logo ali', email = 'adniministrador@gmail.com',password = 'a',is_superuser = True)
		user_super.set_password('passaumdolar')
		user_super.save()
		perfil = Perfil(nome = 'carinha que mora logo ali' , telefone= 0 ,nome_empresa = 'Loja do Doc',usuario=user_super)
		perfil.save()
		
		#user_super.set_password('passaumdolar')
		#user_super.save()
	return render(request, 'decidir_acao.html')

@login_required
def pagina_inicial(request):
	return render(request, 'pagina_inicial.html',{'perfil_logado' : get_perfil_logado(request)})

@login_required
def exibir_perfil(request, perfil_id):

	perfil = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	is_amigos = perfil_logado.contatos.filter(id = perfil.id).exists()
	exist = Convite.exist(perfil , perfil_logado)


	if perfil.id != perfil_logado.id:
		if is_amigos:
			return render(request, 'perfil.html',
				{'perfil' : perfil, 
				'perfil_logado' : get_perfil_logado(request),
				'is_amigos' : True, 'is_convidado' : False, 'is_me' : False})
		else:
			if exist:
				return render(request, 'perfil.html',
					{'perfil' : perfil, 
					'perfil_logado' : get_perfil_logado(request),
					'is_amigos' : False, 'is_convidado' : True, 'is_me' : False})
			else:
				return render(request, 'perfil.html',
					{'perfil' : perfil, 
					'perfil_logado' : get_perfil_logado(request),
					'is_amigos' : False, 'is_convidado' : False, 'is_me' : False})
	else:
		return render(request, 'perfil.html',
				{'perfil' : perfil, 
				'perfil_logado' : get_perfil_logado(request),'is_me' : True})


@login_required
def convidar(request,perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	
	if(perfil_logado.pode_convidar(perfil_a_convidar,perfil_logado)):
		perfil_logado.convidar(perfil_a_convidar)
	
	return  redirect('pagina-inicial')

@login_required
def get_perfil_logado(request):
	return request.user.perfil

@login_required
def desfazer(request,perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_desfazer = Perfil.objects.get(id=perfil_id)
	perfil_logado.desfazer(perfil_logado , perfil_desfazer)
	return redirect('pagina-inicial')


@login_required
def aceitar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.aceitar()
	return redirect('pagina-inicial')

@login_required
def recusar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.delete()
	return redirect('pagina-inicial')

@login_required
def listar_perfis(request):
	logado = get_perfil_logado(request)
	amigos = logado.amigos.all()
	perfis = Perfil.objects.all()

	return render(request, 'lista_de_perfis.html', {'perfis' : perfis,'amigos' : amigos,
		'perfil_logado' : get_perfil_logado(request)})

@login_required
def mudar_senha(request, perfil_id):
	perfil = get_perfil_logado(request)
	return render(request, 'mudar-senha.html', {'perfil_logado' : perfil, 'perfil_id' : perfil_id})