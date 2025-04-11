from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'data_nascimento', 'idade', 'data_cadastro', 'ativo')
    list_filter = ('sexo', 'ativo', 'cidade', 'estado')
    search_fields = ('nome', 'cpf', 'telefone', 'email')
    readonly_fields = ('data_cadastro', 'data_atualizacao')
    fieldsets = (
        ('Informau00e7u00f5es Pessoais', {
            'fields': ('nome', 'data_nascimento', 'sexo', 'cpf')
        }),
        ('Contato', {
            'fields': ('telefone', 'email')
        }),
        ('Endereu00e7o', {
            'fields': ('endereco', 'cidade', 'estado', 'cep')
        }),
        ('Informau00e7u00f5es Adicionais', {
            'fields': ('observacoes', 'ativo', 'data_cadastro', 'data_atualizacao')
        }),
    )