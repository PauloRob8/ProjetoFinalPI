from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=20, null= False)
    nome_empresa = models.CharField(max_length=255, null=False)
    foto_perfil = models.FileField(upload_to="media/perfis/", null = True, default = None)
    contatos = models.ManyToManyField('Perfil',related_name="amigos")
    bloqueados = models.ManyToManyField('Perfil')
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
        is_bloqueado = perfil_convidado.bloqueados.filter(id = perfil_logado.id).exists()
        if not is_bloqueado:
            if perfil_convidado.id == perfil_logado.id:
                return False
            else:
                return True
        else:
            return False
    
    def desfazer(self,perfil_logado , perfil_convidado):
        logado = Perfil.objects.get(id = perfil_logado.id)
        convidado = Perfil.objects.get(id = perfil_convidado.id)
        
        logado.amigos.remove(convidado)
        convidado.amigos.remove(logado)

    def bloquear(self,perfil_logado , perfil_selecionado):
        exist_convite1 = Convite.objects.filter(solicitante = perfil_logado.id, convidado = perfil_selecionado.id).exists()
        exist_convite2 = Convite.objects.filter(solicitante = perfil_selecionado.id, convidado = perfil_logado.id).exists()
        is_amigos = perfil_logado.contatos.filter(id = perfil_selecionado.id).exists()
        
        if exist_convite1:
            Convite.objects.get(solicitante= perfil_logado.id,convidado = perfil_selecionado.id).delete()
        if exist_convite2:
            Convite.objects.get(solicitante= perfil_selecionado.id,convidado = perfil_logado.id).delete()
        
        if is_amigos:
            perfil_logado.contatos.remove(perfil_selecionado)
            perfil_selecionado.contatos.remove(perfil_logado)
        
        perfil_logado.bloqueados.add(perfil_selecionado)
    
    def desbloquear(self,perfil_logado , perfil_desbloqueado):
        desbloquear = perfil_logado.bloqueados.get(id = perfil_desbloqueado.id)
        perfil_logado.bloqueados.remove(desbloquear)

class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):        
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()


    def exist(perfil_convidado, perfil_logado ):
        logado = Convite.objects.filter(solicitante = perfil_logado.id).exists()
        convidado = Convite.objects.filter(convidado = perfil_convidado.id).exists()
        logado_reverse = Convite.objects.filter(solicitante = perfil_convidado.id).exists()
        convidado_reverse = Convite.objects.filter(convidado = perfil_logado.id).exists()
        if convidado or convidado_reverse:
            if logado or logado_reverse:
                return True
    

