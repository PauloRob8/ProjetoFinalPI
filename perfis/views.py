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
	return render(request, 'decidir_acao.html')

@login_required
def pagina_inicial(request):
	logado = get_perfil_logado(request)
	convites = Convite.objects.all()
	return render(request, 'pagina_inicial.html',{'perfil_logado' : logado, 'convites_espera' : convites})

@login_required
def exibir_perfil(request, perfil_id):

	perfil = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	is_amigos = perfil_logado.contatos.filter(id = perfil.id).exists()
	exist = Convite.exist(perfil , perfil_logado)
	
	bloqueado1 = perfil.bloqueados.filter(id = perfil_logado.id).exists()
	bloqueado2 = perfil_logado.bloqueados.filter(id = perfil.id).exists()
	user = perfil_logado.usuario
	is_super = user.is_superuser

	bloqueado = False
	if bloqueado1 or bloqueado2:
		bloqueado = True

	if perfil.id != perfil_logado.id:
		if is_super:
			return render(request, 'perfil_issuper.html',
					{'perfil' : perfil, 
					'perfil_logado' : get_perfil_logado(request),
					'is_amigos' : is_amigos, 'is_convidado' : exist, 'is_me' : False, 'is_block' : bloqueado})
		else:
			return render(request, 'perfil_notsuper.html',
					{'perfil' : perfil, 
					'perfil_logado' : get_perfil_logado(request),
					'is_amigos' : is_amigos, 'is_convidado' : exist, 'is_me' : False, 'is_block' : bloqueado})
	else:
		return render(request, 'perfil_notsuper.html',
				{'perfil' : perfil, 
				'perfil_logado' : get_perfil_logado(request),'is_me' : True})



@login_required
def convidar(request,perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	perfil_bloqueado = perfil_a_convidar.bloqueados.filter(id = perfil_logado.id).exists()
	
	if not perfil_bloqueado:
		if perfil_logado.pode_convidar(perfil_a_convidar,perfil_logado):
			perfil_logado.convidar(perfil_a_convidar)
	
	return  redirect('pagina-inicial')

@login_required
def desfazer(request,perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_desfazer = Perfil.objects.get(id=perfil_id)
	perfil_logado.desfazer(perfil_logado , perfil_desfazer)
	return redirect('pagina-inicial')

@login_required
def bloquear(request,perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_bloquear = Perfil.objects.get(id=perfil_id)
	perfil_logado.bloquear(perfil_logado,perfil_bloquear)
	return redirect('pagina-inicial')

@login_required
def desbloquear(request,perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_desbloquear = Perfil.objects.get(id=perfil_id)
	perfil_logado.desbloquear(perfil_logado,perfil_desbloquear)
	return redirect('pagina-inicial')

@login_required
def get_perfil_logado(request):
	return request.user.perfil

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