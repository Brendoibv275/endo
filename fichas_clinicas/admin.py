from django.contrib import admin
from .models import FichaClinica, SessaoAtendimento

class SessaoAtendimentoInline(admin.TabularInline):
    model = SessaoAtendimento
    extra = 0

@admin.register(FichaClinica)
class FichaClinicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'dente', 'data_abertura', 'queixa_principal', 'status')
    list_filter = ('status', 'data_abertura')
    search_fields = ('paciente__nome', 'dente', 'queixa_principal', 'diagnostico')
    date_hierarchy = 'data_abertura'
    inlines = [SessaoAtendimentoInline]

@admin.register(SessaoAtendimento)
class SessaoAtendimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ficha', 'data_sessao', 'realizado_por')
    list_filter = ('data_sessao',)
    search_fields = ('ficha__paciente__nome', 'procedimentos')
    date_hierarchy = 'data_sessao'