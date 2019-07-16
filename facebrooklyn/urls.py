"""connectedin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from perfis import views
from perfis.views import *
from usuarios.views import *
from post import views
from django.contrib.auth import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.decidir_acao,name='decidir'),
    path('desativado', views.perfil_desativado , name='desativado'),
    path('desativado/<int:perfil_id>/ativar', views.perfil_active, name='ativar'),
    path('pagina-inicial/', views.pagina_inicial,name='pagina-inicial'),
    path('pagina-inicial/meus-posts', views.meus_posts,name='meus-posts'),
    path('pagina-inicial/buscar', PesquisarUsuarioView.as_view(),name='buscar'),
    path('pagina-inicial/<int:post_id>', views.visualizar_post,name='post'),
    path('pagina-inicial/<int:post_id>/marcar', views.FazerMarcacaoView.as_view(),name='marcar'),
    path('pagina-inicial/<int:post_id>/comentar', views.FazerComentarioView.as_view(),name='comentar'),
    path('pagina-inicial/reagir/<int:post_id>/<int:cod_reacao>', views.reagir_post,name='reagir'),
    path('pagina-inicial/deletar/<int:post_id>', views.excluir_postagem,name='excluir_post'),
    path('pagina-inicial/compartilha/<int:post_id>', views.compartilha_post,name='compartilha'),
    path('pagina-inicial/editar/<int:post_id>', views.editar_post,name='editar'),
    path('pagina-inicial/editar/<int:post_id>/concluir', views.EditarPostView.as_view(),name='concluir-editar'),
    path('criar-post/', views.nova_postagem, name='criar_post'),
    path('criar-post/postar',views.FazerPostView.as_view(), name='postar'),
    path('listarperfis/', views.listar_perfis, name='listaperfis'),
    path('perfil/<int:perfil_id>', views.exibir_perfil, name='exibir'),
    path('perfil/<int:perfil_id>/tornar-super', views.tornar_super, name='tornar'),
    path('perfil/<int:perfil_id>/mudar-senha', views.mudar_senha, name='mudar-senha'),
    path('perfil/<int:perfil_id>/mudar-senha/confirma', MudarSenhaView.as_view(), name='confirma-mudanca'),
    path('perfil/<int:perfil_id>/bloquear', views.bloquear, name='bloquear'),
    path('perfil/<int:perfil_id>/desativar', views.desativar_perfil, name='desativar'),
    path('perfil/<int:perfil_id>/desbloquear', views.desbloquear, name='desbloquear'),
    path('perfil/<int:perfil_id>/convidar',views.convidar, name='convidar'),
    path('perfil/<int:perfil_id>/desfazer',views.desfazer, name='desfazer'),
    path('convite/<int:convite_id>/aceitar',views.aceitar, name='aceitar'),
    path('convite/<int:convite_id>/recusar',views.recusar, name='recusar'),
    path('registrar/', RegistrarUsuarioView.as_view(), name="registrar"),
    path('login/',v.LoginView.as_view(template_name='login.html'),name = 'login'),
    path('logout/',v.LogoutView.as_view(template_name='decidir_acao.html'),name='logout'),
]

