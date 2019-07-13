from django.shortcuts import render
from perfis.models import Perfil, Convite
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
# Create your views here.

@login_required
def index(request):
	return render(request, 'index.html',{'perfis' : Perfil.objects.all(),
										 'perfil_logado' : get_perfil_logado(request)})

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
	
	return  redirect('index')

@login_required
def get_perfil_logado(request):
	return request.user.perfil

@login_required
def desfazer(request,perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_desfazer = Perfil.objects.get(id=perfil_id)
	perfil_logado.desfazer(perfil_logado , perfil_desfazer)
	return redirect('index')


@login_required
def aceitar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.aceitar()
	return redirect('index')

@login_required
def recusar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.delete()
	return redirect('index')

@login_required
def listar_perfis(request):
	return render(request, 'lista_de_perfis.html', {'perfis' : Perfil.objects.all(), 
		'perfil_logado' : get_perfil_logado(request)})

@login_required
def mudar_senha(request, perfil_id):
	perfil = get_perfil_logado(request)
	return render(request, 'mudar-senha.html', {'perfil_logado' : perfil, 'perfil_id' : perfil_id})