from django.db import models
from django.contrib.auth.models import User


class Evento(models.Model):
    criador = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=200, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição')
    data_inicio = models.DateField(verbose_name='Data de inicio')
    data_termino = models.DateField(verbose_name='Data de término')
    carga_horaria = models.IntegerField(verbose_name='Carga horaria')
    logo = models.FileField(upload_to="logos")
    participantes = models.ManyToManyField(
        User, verbose_name="Participantes", null=True, 
        related_name='evento_participante'
    )

    #paleta de cores
    cor_principal = models.CharField(max_length=7)
    cor_secundaria = models.CharField(max_length=7)
    cor_fundo = models.CharField(max_length=7, verbose_name='cor de fundo')
    

    def __str__(self):
        return self.nome


class Certificado(models.Model):
    certificado = models.ImageField("Certificado", 
                                    upload_to='certificados/%Y/%m')
    participante = models.ForeignKey(User, verbose_name="Participante", 
                                     on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, verbose_name="Evento", 
                               on_delete=models.DO_NOTHING,
                               related_name='certificado_evento')
    
    def __str__(self):
        return self.participante.username