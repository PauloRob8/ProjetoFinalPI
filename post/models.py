from django.db import models
from perfis.models import Perfil

# Create your models here.
class Post(models.Model):
    conteudo = models.CharField(max_length=50, null=False)
    autor = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='meus_posts' )
    imagem = models.FileField(upload_to="media/post/", null =True, default = None)
    data = models.DateField(auto_now_add=True, null = True)
    amei = models.IntegerField()
    odiei = models.IntegerField()
    triste = models.IntegerField()
    legal = models.IntegerField()

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