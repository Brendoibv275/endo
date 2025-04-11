from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Paciente, UserProfile, TeamMember
from .forms import PacienteForm, PacienteBuscaForm, UserRegistrationForm, TeamMemberForm, ClinicaUserForm
from fichas_clinicas.models import FichaClinica, SessaoAtendimento
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class ClinicaMixin:
    def get_queryset(self):
        # Obtém o queryset original
        queryset = super().get_queryset()
        
        # Verifica se o usuário está logado
        if not self.request.user.is_authenticated:
            return queryset.none()
        
        # Se for superusuário, retorna todos os registros
        if self.request.user.is_superuser:
            return queryset
        
        # Obtém a clínica do usuário
        try:
            clinica = self.request.user.profile.clinica
            if clinica is None:
                return queryset.none()
            
            # Se for líder de equipe, mostra todos os pacientes da clínica
            if self.request.user.profile.is_team_leader:
                return queryset.filter(clinica=clinica)
            
            # Se não for líder, mostra apenas seus próprios pacientes
            return queryset.filter(clinica=clinica, responsavel=self.request.user)
        except:
            return queryset.none()

    def form_valid(self, form):
        # Define a clínica e o responsável antes de salvar o formulário
        if not form.instance.clinica_id and not self.request.user.is_superuser:
            form.instance.clinica = self.request.user.profile.clinica
            form.instance.responsavel = self.request.user
        return super().form_valid(form)

class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'pacientes/paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Simplificar a lógica para garantir que sempre retorne pacientes
        # Verificar primeiro se o usuário tem privilégios administrativos
        if self.request.user.is_superuser or self.request.user.is_staff:
            return queryset
        
        # Se não for admin, verificar se é líder de equipe (de forma segura)
        is_team_leader = False
        try:
            if hasattr(self.request.user, 'profile') and self.request.user.profile.is_team_leader:
                is_team_leader = True
            elif hasattr(self.request.user, 'profile') and hasattr(self.request.user.profile, 'funcao') and self.request.user.profile.funcao:
                if hasattr(self.request.user.profile.funcao, 'nome') and self.request.user.profile.funcao.nome == 'Líder de Equipe':
                    is_team_leader = True
        except:
            pass
            
        if is_team_leader:
            # Líderes veem todos os pacientes da clínica se tiver clínica associada
            try:
                if hasattr(self.request.user, 'profile') and hasattr(self.request.user.profile, 'clinica') and self.request.user.profile.clinica:
                    return queryset.filter(clinica=self.request.user.profile.clinica)
            except:
                pass
        
        # Caso padrão: veja apenas seus próprios pacientes
        return queryset.filter(responsavel=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_busca'] = PacienteBuscaForm(initial={'termo_busca': self.request.GET.get('termo_busca', '')})
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class PacienteDetailView(LoginRequiredMixin, ClinicaMixin, DetailView):
    model = Paciente
    template_name = 'pacientes/paciente_detail.html'
    context_object_name = 'paciente'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.clinica != self.request.user.profile.clinica and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    success_url = reverse_lazy('pacientes:paciente_lista')

    def form_valid(self, form):
        form.instance.responsavel = self.request.user
        form.instance.clinica = self.request.user.profile.clinica
        return super().form_valid(form)

class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    success_url = reverse_lazy('pacientes:paciente_lista')

    def get_queryset(self):
        queryset = super().get_queryset()
        # Verificar se o usuário tem perfil e função associados
        if hasattr(self.request.user, 'profile') and hasattr(self.request.user.profile, 'funcao') and self.request.user.profile.funcao and hasattr(self.request.user.profile.funcao, 'nome') and self.request.user.profile.funcao.nome == 'Líder de Equipe':
            return queryset.filter(clinica=self.request.user.profile.clinica)
        return queryset.filter(responsavel=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_team_leader = hasattr(request.user, 'profile') and hasattr(request.user.profile, 'funcao') and request.user.profile.funcao and hasattr(request.user.profile.funcao, 'nome') and request.user.profile.funcao.nome == 'Líder de Equipe'
        if obj.responsavel != request.user and not is_team_leader:
            return HttpResponseForbidden("Você não tem permissão para editar este paciente.")
        return super().dispatch(request, *args, **kwargs)

class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'pacientes/paciente_confirm_delete.html'
    success_url = reverse_lazy('pacientes:paciente_lista')

    def get_queryset(self):
        queryset = super().get_queryset()
        # Verificar se o usuário tem perfil e função associados
        if hasattr(self.request.user, 'profile') and hasattr(self.request.user.profile, 'funcao') and self.request.user.profile.funcao and hasattr(self.request.user.profile.funcao, 'nome') and self.request.user.profile.funcao.nome == 'Líder de Equipe':
            return queryset.filter(clinica=self.request.user.profile.clinica)
        return queryset.filter(responsavel=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_team_leader = hasattr(request.user, 'profile') and hasattr(request.user.profile, 'funcao') and request.user.profile.funcao and hasattr(request.user.profile.funcao, 'nome') and request.user.profile.funcao.nome == 'Líder de Equipe'
        if obj.responsavel != request.user and not is_team_leader:
            return HttpResponseForbidden("Você não tem permissão para excluir este paciente.")
        return super().dispatch(request, *args, **kwargs)

@login_required
def paciente_detalhe(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    # Processar o agendamento de sessões
    if request.method == 'POST':
        # Verificar se o paciente tem pelo menos uma ficha clínica
        fichas = FichaClinica.objects.filter(paciente=paciente)
        if not fichas.exists():
            messages.error(request, "Este paciente não possui fichas clínicas. Crie uma ficha antes de agendar uma sessão.")
            return redirect('pacientes:paciente_detalhe', pk=paciente.pk)
        
        # Obter os dados do formulário
        data_sessao = request.POST.get('data_sessao')
        hora_sessao = request.POST.get('hora_sessao')
        tipo_sessao = request.POST.get('tipo_sessao')
        observacoes = request.POST.get('observacoes')
        
        # Usar a ficha mais recente do paciente
        ficha_mais_recente = fichas.latest('data_abertura')
        
        # Criar o agendamento
        try:
            # Converter a string de data para objeto date
            data_convertida = datetime.strptime(data_sessao, '%Y-%m-%d').date()
            
            # Converter a string de hora para objeto time (se fornecido)
            hora_convertida = None
            if hora_sessao:
                hora_convertida = datetime.strptime(hora_sessao, '%H:%M').time()
            
            # Criar a sessão
            sessao = SessaoAtendimento.objects.create(
                ficha=ficha_mais_recente,
                data_sessao=data_convertida,
                hora_sessao=hora_convertida,
                tipo_sessao=tipo_sessao,
                procedimentos="Agendamento: " + (observacoes or "Sessão agendada"),
                observacoes=observacoes,
                realizado_por=request.user
            )
            
            messages.success(request, f"Sessão agendada com sucesso para {data_sessao} às {hora_sessao}.")
            return redirect('pacientes:paciente_detalhe', pk=paciente.pk)
        except Exception as e:
            messages.error(request, f"Erro ao agendar sessão: {str(e)}")
    
    # Renderizar a página
    context = {
        'paciente': paciente,
    }
    return render(request, 'pacientes/paciente_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('pacientes:paciente_lista')
    else:
        form = UserRegistrationForm()
    return render(request, 'pacientes/register.html', {'form': form})

@login_required
def paciente_list(request):
    # Verifica se o usuário é líder de equipe
    is_team_leader = hasattr(request.user, 'userprofile') and request.user.userprofile.is_team_leader
    
    # Se for líder de equipe, mostra todos os pacientes da equipe
    if is_team_leader:
        team_members = User.objects.filter(
            teammember__team_leader=request.user
        )
        pacientes = Paciente.objects.filter(
            responsavel__in=[request.user] + list(team_members)
        )
    else:
        # Se não for líder, mostra apenas seus próprios pacientes
        pacientes = Paciente.objects.filter(responsavel=request.user)
    
    form = PacienteBuscaForm(request.GET)
    if form.is_valid():
        termo = form.cleaned_data['termo_busca']
        if termo:
            pacientes = pacientes.filter(
                nome__icontains=termo
            ) | pacientes.filter(
                cpf__icontains=termo
            ) | pacientes.filter(
                telefone__icontains=termo
            )
    
    return render(request, 'pacientes/paciente_list.html', {
        'pacientes': pacientes,
        'form': form,
        'is_team_leader': is_team_leader
    })

@login_required
def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.responsavel = request.user
            paciente.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('pacientes:paciente_lista')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/paciente_form.html', {'form': form})

@login_required
def paciente_update(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    # Verifica se o usuário tem permissão para editar o paciente
    if paciente.responsavel != request.user and not (
        hasattr(request.user, 'userprofile') and 
        request.user.userprofile.is_team_leader and
        paciente.responsavel.teammember_set.filter(team_leader=request.user).exists()
    ):
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente atualizado com sucesso!')
            return redirect('pacientes:paciente_lista')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/paciente_form.html', {'form': form})

@login_required
def team_management(request):
    if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_team_leader:
        return HttpResponseForbidden()
    
    team_members = TeamMember.objects.filter(team_leader=request.user)
    
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.team_leader = request.user
            member.save()
            messages.success(request, 'Membro adicionado à equipe com sucesso!')
            return redirect('team_management')
    else:
        form = TeamMemberForm()
    
    return render(request, 'pacientes/team_management.html', {
        'team_members': team_members,
        'form': form
    })

@login_required
def remove_team_member(request, pk):
    if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_team_leader:
        return HttpResponseForbidden()
    
    member = get_object_or_404(TeamMember, pk=pk, team_leader=request.user)
    member.delete()
    messages.success(request, 'Membro removido da equipe com sucesso!')
    return redirect('team_management')

@login_required
def add_team_member(request):
    if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_team_leader:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.team_leader = request.user
            member.save()
            messages.success(request, 'Membro adicionado à equipe com sucesso!')
            return redirect('team_management')
    else:
        form = TeamMemberForm()
    
    return render(request, 'pacientes/add_team_member.html', {
        'form': form
    })

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'pacientes/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        if not form.cleaned_data['is_admin']:
            messages.info(self.request, 'Seu cadastro foi recebido. Um administrador irá aprovar seu acesso em breve.')
        return response

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Login realizado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return self.next_page

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Logout realizado com sucesso!')
        return super().dispatch(request, *args, **kwargs)

@login_required
def clinica_management(request):
    # Verificar se o usuário é líder de equipe (de forma segura)
    is_team_leader = False
    try:
        if hasattr(request.user, 'profile'):
            if request.user.profile.is_team_leader:
                is_team_leader = True
            elif hasattr(request.user.profile, 'funcao') and request.user.profile.funcao:
                if hasattr(request.user.profile.funcao, 'nome') and request.user.profile.funcao.nome == 'Líder de Equipe':
                    is_team_leader = True
    except:
        pass
    
    if not is_team_leader:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    
    # Verificar se o usuário tem uma clínica associada
    clinica = None
    try:
        if hasattr(request.user, 'profile') and hasattr(request.user.profile, 'clinica'):
            clinica = request.user.profile.clinica
    except:
        pass
    
    if not clinica:
        messages.error(request, "Você não tem uma clínica associada ao seu perfil.")
        return redirect('dashboard')
    
    # Buscar membros da clínica
    try:
        membros = UserProfile.objects.filter(
            clinica=clinica,
            user__teammember__team_leader=request.user
        )
    except:
        membros = []
    
    return render(request, 'pacientes/clinica_management.html', {
        'clinica': clinica,
        'membros': membros
    })

@login_required
def add_clinica_user(request):
    # Verificar se o usuário é líder de equipe (de forma segura)
    is_team_leader = False
    try:
        if hasattr(request.user, 'profile'):
            if request.user.profile.is_team_leader:
                is_team_leader = True
            elif hasattr(request.user.profile, 'funcao') and request.user.profile.funcao:
                if hasattr(request.user.profile.funcao, 'nome') and request.user.profile.funcao.nome == 'Líder de Equipe':
                    is_team_leader = True
    except:
        pass
    
    if not is_team_leader:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    
    # Verificar se o usuário tem uma clínica associada
    clinica = None
    try:
        if hasattr(request.user, 'profile') and hasattr(request.user.profile, 'clinica'):
            clinica = request.user.profile.clinica
    except:
        pass
    
    if not clinica:
        messages.error(request, "Você não tem uma clínica associada ao seu perfil.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ClinicaUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                if not hasattr(user, 'profile'):
                    UserProfile.objects.create(user=user)
                user.profile.clinica = clinica
                user.save()
                user.profile.save()
                
                # Adiciona o usuário à equipe do líder
                TeamMember.objects.create(
                    team_leader=request.user,
                    member=user
                )
                
                messages.success(request, 'Usuário adicionado com sucesso!')
                return redirect('pacientes:clinica_management')
            except Exception as e:
                messages.error(request, f'Erro ao adicionar usuário: {str(e)}')
    else:
        form = ClinicaUserForm()
    
    return render(request, 'pacientes/add_clinica_user.html', {
        'form': form
    })

@login_required
def remove_clinica_user(request, user_id):
    # Verificar se o usuário é líder de equipe (de forma segura)
    is_team_leader = False
    try:
        if hasattr(request.user, 'profile'):
            if request.user.profile.is_team_leader:
                is_team_leader = True
            elif hasattr(request.user.profile, 'funcao') and request.user.profile.funcao:
                if hasattr(request.user.profile.funcao, 'nome') and request.user.profile.funcao.nome == 'Líder de Equipe':
                    is_team_leader = True
    except:
        pass
    
    if not is_team_leader:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    
    try:
        user = get_object_or_404(User, id=user_id)
        # Verifica se o usuário pertence à equipe do líder
        if not TeamMember.objects.filter(team_leader=request.user, member=user).exists():
            return HttpResponseForbidden("Você não tem permissão para remover este usuário.")
        
        user.delete()
        messages.success(request, 'Usuário removido com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao remover usuário: {str(e)}')
    
    return redirect('pacientes:clinica_management')