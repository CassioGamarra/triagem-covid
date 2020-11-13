from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash
    
class Triagem(models.Model):

    codigo = models.CharField(_('Código da triagem *'), unique=True, max_length=20, help_text='* Campos obrigatórios')
    data = models.DateField(_('Data da consulta *'), help_text='dd/mm/aaaa')
    hora = models.TimeField(_('Hora da consulta *'), help_text='hh:mm')
    nome = models.CharField(_('Nome Completo *'), max_length=50)
    idade = models.PositiveIntegerField(_('Idade *'), validators=[MaxValueValidator(100),])
    altura = models.DecimalField(_('Altura *'), decimal_places=2, max_digits=15)
    peso = models.DecimalField(_('Peso *'), decimal_places=2, max_digits=15)
    imc = models.DecimalField(_('IMC *'), decimal_places=2, max_digits=15)
    #Valores para análise
    febre = models.BooleanField(_('Tem febre?'))
    dor_cabeca = models.BooleanField(_('Tem dor de cabeça?'))
    secrecao_espirro = models.BooleanField(_('Tem secreção nasal ou espirros?'))
    dor_garganta = models.BooleanField(_('Tem dor/irritação de garganta?'))
    tosse_seca = models.BooleanField(_('Tem tosse seca?'))
    dificuldade_respiratoria = models.BooleanField(_('Tem dificuldade respiratória?'))
    dores_corpo = models.BooleanField(_('Tem dores no corpo?'))
    diarreia = models.BooleanField(_('Tem diarreia?'))
    viagem_covid = models.BooleanField(_('Viajou, nos últimos 14 dias, para algum local com casos confirmados de COVID-19?'))
    contato_covid = models.BooleanField(_('Esteve em contato, nos últimos 14 dias, com um caso diagnosticado com COVID-19?'))
    resultado = models.PositiveIntegerField(_('Resultado'))

    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering            =   ['-data','-hora','nome']
        verbose_name        =   ('triagem')
        verbose_name_plural =   ('triagens')
        unique_together     =   ['codigo', 'data', 'hora'] #criando chave primária composta no BD

    def __str__(self):
        return "Triagem: %s - Data: %s." % (self.codigo, self.data)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.codigo = self.codigo.upper()
        super(Triagem, self).save(*args, **kwargs)

    @property
    def get_update_url(self):
        return reverse('triagem_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('triagem_delete', args=[str(self.id)])
    
    @property
    def get_visualiza_url(self):
        return reverse('triagem_detail', args=[str(self.id)])
