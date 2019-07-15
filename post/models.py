from django.db import models
from perfis.models import Perfil

# Create your models here.
class Post(models.Model):
    conteudo = models.CharField(max_length=300, null=False)
    autor = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='meus_posts' )
    amei = models.IntegerField()
    odiei = models.IntegerField()
    triste = models.IntegerField()
    legal = models.IntegerField()

    def criar_post(self,perfil_logado,texto):
        post_cria = Post(conteudo = texto, amei = 0, odiei = 0, triste = 0, legal = 0)
        post_cria.save()
        post = [post_cria]
        perfil_logado.meus_posts.set(post)

    def reagir(self,perfil_logado, opcao):
        if opcao == 1:
            self.amei += 1
            self.save
        elif opcao == 2:
            self.odiei += 1
            self.save
        elif opcao == 3:
            self.triste += 1
            self.save
        elif opcao == 4:
            self.legal += 1
            self.save