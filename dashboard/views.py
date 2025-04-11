from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Q
from django.utils import timezone
from datetime import timedelta, datetime
import calendar
import json

from pacientes.models import Paciente
from fichas_clinicas.models import FichaClinica, SessaoAtendimento

@login_required
def dashboard_view(request):
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # Verificar se é líder de equipe ou admin
    is_admin = request.user.is_superuser
    is_team_leader = False
    try:
        if hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
            is_team_leader = True
        elif hasattr(request.user, 'profile') and hasattr(request.user.profile, 'funcao') and request.user.profile.funcao:
            if hasattr(request.user.profile.funcao, 'nome') and request.user.profile.funcao.nome == 'Líder de Equipe':
                is_team_leader = True
    except:
        pass
    
    # Filtrar por pacientes do usuário atual, a menos que seja admin ou líder
    if is_admin:
        pacientes_query = Paciente.objects.all()
        fichas_query = FichaClinica.objects.all()
        sessoes_query = SessaoAtendimento.objects.all()
    elif is_team_leader:
        try:
            clinica = request.user.profile.clinica
            pacientes_query = Paciente.objects.filter(clinica=clinica)
            fichas_query = FichaClinica.objects.filter(paciente__clinica=clinica)
            sessoes_query = SessaoAtendimento.objects.filter(ficha__paciente__clinica=clinica)
        except:
            pacientes_query = Paciente.objects.filter(responsavel=request.user)
            fichas_query = FichaClinica.objects.filter(paciente__responsavel=request.user)
            sessoes_query = SessaoAtendimento.objects.filter(ficha__paciente__responsavel=request.user)
    else:
        pacientes_query = Paciente.objects.filter(responsavel=request.user)
        fichas_query = FichaClinica.objects.filter(paciente__responsavel=request.user)
        sessoes_query = SessaoAtendimento.objects.filter(ficha__paciente__responsavel=request.user)
    
    # Estatísticas principais
    total_pacientes = pacientes_query.count()
    total_fichas = fichas_query.count()
    fichas_em_andamento = fichas_query.filter(status='E').count()
    sessoes_hoje = sessoes_query.filter(data_sessao=hoje).count()
    
    # Obter próximas sessões
    proximas_sessoes = sessoes_query.filter(
        data_sessao__gte=hoje
    ).order_by('data_sessao', 'hora_sessao')[:5]
    
    # Distribuição de tipos de tratamentos
    tipos_tratamento = {}
    # Verificando campos específicos em fichas ou procedimentos para classificar
    fichas_endodontia = fichas_query.filter(
        Q(queixa_principal__icontains='canal') | 
        Q(queixa_principal__icontains='endo') |
        Q(sessoes__procedimentos__icontains='canal')
    ).distinct().count()
    
    fichas_restauracao = fichas_query.filter(
        Q(queixa_principal__icontains='restaura') | 
        Q(sessoes__procedimentos__icontains='restaura')
    ).distinct().count()
    
    fichas_avaliacao = fichas_query.filter(
        Q(queixa_principal__icontains='avalia') | 
        Q(sessoes__procedimentos__icontains='avalia')
    ).distinct().count()
    
    fichas_retratamento = fichas_query.filter(
        Q(queixa_principal__icontains='retratamento') | 
        Q(sessoes__procedimentos__icontains='retratamento')
    ).distinct().count()
    
    # Totais para os gráficos
    total_tipos = fichas_endodontia + fichas_restauracao + fichas_avaliacao + fichas_retratamento
    if total_tipos == 0:
        total_tipos = 1  # Evitar divisão por zero
    
    # Porcentagens arredondadas
    tipos_tratamento = {
        'endodontia': round((fichas_endodontia / total_tipos) * 100),
        'restauracoes': round((fichas_restauracao / total_tipos) * 100),
        'avaliacoes': round((fichas_avaliacao / total_tipos) * 100),
        'retratamentos': round((fichas_retratamento / total_tipos) * 100)
    }
    
    # Atendimentos mensais (últimos 6 meses)
    atendimentos_mensais = []
    labels_meses = []
    for i in range(5, -1, -1):
        # Calcular mês
        mes_idx = (mes_atual - i - 1) % 12 + 1
        ano = ano_atual if mes_idx > mes_atual else ano_atual - 1
        
        # Nome do mês
        mes_nome = calendar.month_name[mes_idx][:3]
        if mes_idx == mes_atual:
            mes_nome += " (atual)"
        
        # Contar atendimentos
        inicio_mes = datetime(ano, mes_idx, 1).date()
        if mes_idx == 12:
            fim_mes = datetime(ano+1, 1, 1).date() - timedelta(days=1)
        else:
            fim_mes = datetime(ano, mes_idx+1, 1).date() - timedelta(days=1)
        
        qtd_atendimentos = sessoes_query.filter(
            data_sessao__gte=inicio_mes, 
            data_sessao__lte=fim_mes
        ).count()
        
        atendimentos_mensais.append(qtd_atendimentos)
        labels_meses.append(mes_nome)
    
    # Panorama de procedimentos no mês atual
    inicio_mes_atual = datetime(ano_atual, mes_atual, 1).date()
    
    if mes_atual == 12:
        fim_mes_atual = datetime(ano_atual+1, 1, 1).date() - timedelta(days=1)
    else:
        fim_mes_atual = datetime(ano_atual, mes_atual+1, 1).date() - timedelta(days=1)
    
    tratamento_canal = sessoes_query.filter(
        data_sessao__range=(inicio_mes_atual, fim_mes_atual),
        procedimentos__icontains='canal'
    ).count()
    
    retratamentos = sessoes_query.filter(
        data_sessao__range=(inicio_mes_atual, fim_mes_atual),
        procedimentos__icontains='retratamento'
    ).count()
    
    urgencias = sessoes_query.filter(
        data_sessao__range=(inicio_mes_atual, fim_mes_atual),
        procedimentos__icontains='urgência'
    ).count()
    
    avaliacoes = sessoes_query.filter(
        data_sessao__range=(inicio_mes_atual, fim_mes_atual),
        procedimentos__icontains='avaliação'
    ).count()
    
    procedimentos_dados = [tratamento_canal, retratamentos, urgencias, avaliacoes]
    
    context = {
        'total_pacientes': total_pacientes,
        'total_fichas': total_fichas,
        'fichas_em_andamento': fichas_em_andamento,
        'sessoes_recentes': sessoes_hoje,
        'proximas_sessoes': proximas_sessoes,
        'tratamentos_dados': json.dumps(list(tipos_tratamento.values())),
        'tratamentos_labels': json.dumps(list(tipos_tratamento.keys())),
        'atendimentos_mensais': json.dumps(atendimentos_mensais),
        'atendimentos_labels': json.dumps(labels_meses),
        'procedimentos_dados': json.dumps(procedimentos_dados),
    }
    
    return render(request, 'dashboard/dashboard.html', context)