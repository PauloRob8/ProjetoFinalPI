from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=20, null= False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('Perfil',related_name="amigos")
    usuario = models.OneToOneField(User, related_name="perfil",on_delete = models.CASCADE)

    @property
    def email(self):
        return self.usuario.email

    def __str__(self):
        return self.nome

    def convidar(self, perfil_convidado):
        convite = Convite(solicitante=self,convidado = perfil_convidado)
        convite.save()

    def pode_convidar(self, perfil_convidado, perfil_logado):
        if perfil_convidado.id == perfil_logado.id:
            return False
        else:
            return True
    
    def desfazer(self,perfil_logado , perfil_convidado):
        logado = Perfil.objects.get(id = perfil_logado.id)
        convidado = Perfil.objects.get(id = perfil_convidado.id)
        
        logado.amigos.remove(convidado)
        convidado.amigos.remove(logado)

class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):        
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()


    def exist(perfil_convidado, perfil_logado ):
        logado = Convite.objects.filter(solicitante = perfil_logado).exists()
        convidado = Convite.objects.filter(convidado = perfil_convidado).exists()
        logado_reverse = Convite.objects.filter(solicitante = perfil_convidado).exists()
        convidado_reverse = Convite.objects.filter(convidado = perfil_logado).exists()
        if convidado or convidado_reverse:
            if logado or logado_reverse:
                return True
    

