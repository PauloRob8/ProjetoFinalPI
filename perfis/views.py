from django.shortcuts import redirect, render
from perfis.models import Perfil, Convite
from post.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib.auth.models import User
from perfis.forms import *


class PesquisarUsuarioView(View):
	template_name = 'pagina_inicial.html'
	
	def get(self,request):
		return redirect('pagina-inicial')
	
	def post(self, request):
		form = PesquisarUsuarioForm(request.POST)
		if form.is_valid():
			logado = get_perfil_logado(request)
			dados_form = form.cleaned_data
			nome = '' + dados_form['nome_buscar']
			perfis_gerais = Perfil.objects.all()
			amigos = logado.amigos.all()
			perfis = []

			for teste in perfis_gerais:
				if nome in teste.nome:
					perfis.append(teste)
			
			quantidade = len(perfis)
		
		return render(request, 'lista_de_perfis.html', {'perfis' : perfis,'amigos' : amigos,
		'perfil_logado' : get_perfil_logado(request), 'quantidade' : quantidade})


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
	convites = Convite.objects.filter(solicitante = logado.id)
	amigos = logado.contatos.all()
	post_mostrar = []
	postagens = Post.objects.all().order_by('data')
	user = logado.usuario
	is_super = user.is_superuser

	for post in postagens:
		if post.autor in amigos or post.autor == logado:
			post_mostrar.append(post)
	
	quantidade = len(post_mostrar)

	return render(request, 'pagina_inicial.html',{'perfil_logado' : logado, 'convites_espera' : convites, 
	'postagens' : post_mostrar, 'quantidade' : quantidade, 'is_super': is_super})

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


	if perfil.id != perfil_logado.id:
		if is_super:
			return render(request, 'perfil_issuper.html',
					{'perfil' : perfil, 
					'perfil_logado' : get_perfil_logado(request),
					'is_amigos' : is_amigos, 'is_convidado' : exist, 'is_me' : False, 'you_is_block' : bloqueado1, 'block_me' : bloqueado2})
		else:
			return render(request, 'perfil_notsuper.html',
					{'perfil' : perfil, 
					'perfil_logado' : get_perfil_logado(request),
					'is_amigos' : is_amigos, 'is_convidado' : exist, 'is_me' : False, 'you_is_block' : bloqueado1, 'block_me' : bloqueado2})
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

@login_required
def nova_postagem(request):
	perfil = get_perfil_logado(request)
	return render(request, 'formulario_post.html',{'perfil_logado' : perfil})