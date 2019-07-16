from django.shortcuts import redirect, render
from perfis.models import Perfil, Convite
from post.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib.auth.models import User
from perfis.forms import *
from django.core.paginator import Paginator


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
	desativado = perfil_is_desactive(request,logado.id)
	if desativado:
		convites = Convite.objects.filter(solicitante = logado.id)
		marcacoes = Marcacoes.objects.all()
		amigos = logado.contatos.all()
		post_mostrar = []
		postagens = Post.objects.all().order_by('-data')
		user = logado.usuario
		is_super = user.is_superuser

		if not is_super:
			for post in postagens:
				if post.autor in amigos or post.autor == logado:
					post_mostrar.append(post)

			quantidade = len(post_mostrar)
		else:
			for post in postagens:
				post_mostrar.append(post)
		
		quantidade = len(post_mostrar)


		paginator = Paginator(post_mostrar, 10)
		page = request.GET.get('page')
		posts = paginator.get_page(page)


		return render(request, 'pagina_inicial.html',{'perfil_logado' : logado, 'convites_espera' : convites, 
		'postagens' : posts, 'quantidade' : quantidade, 'is_super': is_super, 'marcacoes' : marcacoes})
	else:
		return redirect ('desativado')
		

@login_required
def exibir_perfil(request, perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil = Perfil.objects.get(id=perfil_id)
	desativado = perfil_is_desactive(request,perfil_id)
	desativado2 = perfil_is_desactive(request,perfil_logado.id)
	
	if desativado2:
		is_amigos = perfil_logado.contatos.filter(id = perfil.id).exists()
		exist = Convite.exist(perfil , perfil_logado)
		bloqueado1 = perfil.bloqueados.filter(id = perfil_logado.id).exists()
		bloqueado2 = perfil_logado.bloqueados.filter(id = perfil.id).exists()
		user = perfil_logado.usuario
		is_super = user.is_superuser
		outher_user = perfil.usuario
		is_outher_user = outher_user.is_superuser


		if perfil.id != perfil_logado.id:
			return render(request, 'perfil.html',
				{'perfil' : perfil, 
				'perfil_logado' : get_perfil_logado(request),
				'is_amigos' : is_amigos, 'is_convidado' : exist, 'is_me' : False, 'you_is_block' : bloqueado1, 'block_me' : bloqueado2,
				'is_super': is_super, 'outher_super': is_outher_user, 'is_desativado': desativado})
		else:
			return render(request, 'perfil.html',
				{'perfil' : perfil, 
				'perfil_logado' : get_perfil_logado(request),'is_me' : True})
		
	
	return redirect ('desativado')



@login_required
def convidar(request,perfil_id):
	desativado = perfil_is_desactive(request,perfil_id)
	if desativado:
		perfil_logado = get_perfil_logado(request)
		perfil_a_convidar = Perfil.objects.get(id=perfil_id)
		perfil_logado = get_perfil_logado(request)
		perfil_bloqueado = perfil_a_convidar.bloqueados.filter(id = perfil_logado.id).exists()
		
		if not perfil_bloqueado:
			if perfil_logado.pode_convidar(perfil_a_convidar,perfil_logado):
				perfil_logado.convidar(perfil_a_convidar)
		
		return  redirect('pagina-inicial')
	return redirect('desativado')

@login_required
def desfazer(request,perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_desfazer = Perfil.objects.get(id=perfil_id)
	perfil_logado.desfazer(perfil_logado , perfil_desfazer)
	return redirect('pagina-inicial')

@login_required
def bloquear(request,perfil_id):
	desativado = perfil_is_desactive(request,perfil_id)
	if desativado:
		perfil_logado = get_perfil_logado(request)
		perfil_bloquear = Perfil.objects.get(id=perfil_id)
		perfil_logado.bloquear(perfil_logado,perfil_bloquear)
		return redirect('pagina-inicial')
	return redirect('desativado')

@login_required
def desbloquear(request,perfil_id):
	desativado = perfil_is_desactive(request,perfil_id)
	if desativado:
		perfil_logado = get_perfil_logado(request)
		perfil_desbloquear = Perfil.objects.get(id=perfil_id)
		perfil_logado.desbloquear(perfil_logado,perfil_desbloquear)
		return redirect('pagina-inicial')
	return redirect ('desativado')

@login_required
def get_perfil_logado(request):
	return request.user.perfil

@login_required
def aceitar(request, convite_id):
	logado = get_perfil_logado(request)
	desativado = perfil_is_desactive(request,logado.id)
	if desativado:
		convite = Convite.objects.get(id = convite_id)
		convite.aceitar()
		return redirect('pagina-inicial')
	return redirect ('desativado')

@login_required
def recusar(request, convite_id):
	logado = get_perfil_logado(request)
	desativado = perfil_is_desactive(request,logado.id)
	if desativado:
		convite = Convite.objects.get(id = convite_id)
		convite.delete()
		return redirect('pagina-inicial')
	return redirect ('desativado')

@login_required
def listar_perfis(request):
	logado = get_perfil_logado(request)
	desativado = perfil_is_desactive(request,logado.id)
	if desativado:
		logado = get_perfil_logado(request)
		amigos = logado.amigos.all()
		perfis = Perfil.objects.all()
		user = logado.usuario
		is_super = user.is_superuser

		if is_super:
			return render(request, 'lista_de_perfis.html', {'perfis' : perfis,'amigos' : amigos,
				'perfil_logado' : get_perfil_logado(request)})
		else:
			return redirect('pagina-inicial')
	return redirect('desativado')
		

@login_required
def mudar_senha(request, perfil_id):
	logado = get_perfil_logado(request)
	desativado = perfil_is_desactive(request,logado.id)
	if desativado:
		perfil = get_perfil_logado(request)
		return render(request, 'mudar-senha.html', {'perfil_logado' : perfil, 'perfil_id' : perfil_id})
	return redirect('desativado')

@login_required
def nova_postagem(request):
	logado = get_perfil_logado(request)
	desativado = perfil_is_desactive(request,logado.id)
	if desativado:
		perfil = get_perfil_logado(request)
		return render(request, 'formulario_post.html',{'perfil_logado' : perfil})
	return redirect('desativado')

@login_required
def meus_posts(request):
	logado = get_perfil_logado(request)
	desativado = perfil_is_desactive(request,logado.id)
	if desativado:
		logado = get_perfil_logado(request)
		convites = Convite.objects.filter(solicitante = logado.id)
		amigos = logado.contatos.all()
		post_mostrar = []
		postagens = Post.objects.all().order_by('data')
		user = logado.usuario
		is_super = user.is_superuser

		for post in postagens:
			if is_super and post.autor.id == logado.id:
				post_mostrar.append(post)

		if is_super:
			quantidade = len(post_mostrar)
			return render(request, 'pagina_inicial.html',{'perfil_logado' : logado, 'convites_espera' : convites, 
			'postagens' : post_mostrar, 'quantidade' : quantidade, 'is_super': is_super})
		else:
			return redirect('pagina-inicial')
	return redirect ('desativado')

@login_required
def desativar_perfil(request, perfil_id):
	perfil = Perfil.objects.get(id = perfil_id)
	logado = get_perfil_logado(request)
	
	if perfil.is_active:
		user = logado.usuario
		is_super = user.is_superuser
		outher_user = perfil.usuario
		is_outher_user = outher_user.is_superuser

		if is_super:
			if logado.id != perfil_id:
				if not is_outher_user:
					perfil.is_active = False
					perfil.save()
					return redirect('pagina-inicial')
				else:
					return redirect('pagina-inicial')
			else:
				perfil.is_active = False
				perfil.save()
				return redirect('pagina-inicial')
		else:
			if logado.id == perfil_id:
				perfil.is_active = False
				perfil.save()
				return redirect('pagina-inicial')
	
	return redirect('pagina-inicial')

@login_required
def perfil_is_desactive(request, perfil_id):
	perfil = Perfil.objects.get(id = perfil_id)
	return perfil.is_active

@login_required
def perfil_active(request, perfil_id):
	perfil = Perfil.objects.get(id = perfil_id)
	logado = get_perfil_logado(request)
	if not perfil.is_active:
		user = logado.usuario
		is_super = user.is_superuser
		outher_user = perfil.usuario
		is_outher_user = outher_user.is_superuser

		if is_super:
			if logado.id != perfil_id:
				if not is_outher_user:
					perfil.is_active = True
					perfil.save()
					return redirect('pagina-inicial')
				else:
					return redirect('pagina-inicial')
			else:
				perfil.is_active = True
				perfil.save()
				return redirect('pagina-inicial')
		else:
			if logado.id == perfil_id:
				perfil.is_active = True
				perfil.save()
				return redirect('pagina-inicial')
	
	return redirect('desativado')

@login_required
def perfil_desativado(request):
	logado = get_perfil_logado(request)
	return render(request,'perfil_desativado.html', {'perfil_id': logado.id})

@login_required
def tornar_super(request, perfil_id):
	perfil = Perfil.objects.get(id = perfil_id)
	logado = get_perfil_logado(request)
	user = logado.usuario
	is_super = user.is_superuser
	outher_user = perfil.usuario
	is_outher_user = outher_user.is_superuser

	if not is_outher_user:
		if is_super:
			outher_user.is_superuser = True
			outher_user.save()
	
	return redirect('pagina-inicial')

@login_required
def reagir_post(request,post_id,cod_reacao):
	perfil = get_perfil_logado(request)
	
	if perfil.is_active:
		post = Post.objects.get(id = post_id)
		post.reagir(cod_reacao)
		return render(request, 'post.html', {'post' : post,'perfil_logado' : perfil})
	
	return redirect('desativado')

@login_required
def visualizar_post(request,post_id):
	perfil = get_perfil_logado(request)
	post = Post.objects.get(id = post_id)
	comentarios = Comentario.objects.filter(post = post_id)
	
	if perfil.is_active:
		return render(request, 'post.html', {'post' : post, 'comentarios' : comentarios, 'perfil_logado' : perfil})
	return redirect('desativado')


@login_required
def compartilha_post(request,post_id):
	logado = get_perfil_logado(request)
	post = Post.objects.get(id = post_id)
	texto = post.conteudo

	if logado.is_active:
		post = Post(conteudo = texto, autor = logado, amei = 0, odiei = 0, triste = 0, legal = 0)
		post.save()
		return redirect('pagina-inicial')
	return redirect('desativado')


@login_required
def editar_post(request, post_id):
	logado = get_perfil_logado(request)
	post = Post.objects.get(id = post_id)
	texto = post.conteudo

	if logado.is_active:
		if logado.id == post.autor.id:
			return render(request, 'editar_post.html', {'post_id' : post.id, 'post' : post, 'perfil_logado' : logado})
		
		return redirect('pagina-inicial')
	return redirect('desativado')