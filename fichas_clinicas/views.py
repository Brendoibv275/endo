from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import FichaClinica, SessaoAtendimento, Anamnese, ExameClinico, Diagnostico
from pacientes.models import Paciente
from .forms import (
    FichaClinicaForm, SessaoAtendimentoForm, FichaClinicaBuscaForm,
    FichaClinicaStatusForm, AnamneseForm, ExameClinicoForm, DiagnosticoForm
)

# Views para Fichas Clínicas
class FichaClinicaListView(ListView):
    model = FichaClinica
    template_name = 'fichas_clinicas/ficha_list.html'
    context_object_name = 'fichas'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrar fichas por usuário logado
        if self.request.user.is_superuser:
            pass  # Superadmins veem todas as fichas
        elif hasattr(self.request.user, 'profile') and self.request.user.profile.is_team_leader:
            # Líderes veem fichas de pacientes da sua clínica
            try:
                clinica = self.request.user.profile.clinica
                if clinica:
                    queryset = queryset.filter(paciente__clinica=clinica)
                else:
                    queryset = queryset.filter(paciente__responsavel=self.request.user)
            except:
                queryset = queryset.filter(paciente__responsavel=self.request.user)
        else:
            # Outros usuários veem apenas fichas de seus pacientes
            queryset = queryset.filter(paciente__responsavel=self.request.user)
        
        termo_busca = self.request.GET.get('termo_busca', '')
        
        if termo_busca:
            queryset = queryset.filter(
                Q(paciente__nome__icontains=termo_busca) | 
                Q(dente__icontains=termo_busca) | 
                Q(diagnostico__icontains=termo_busca)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_busca'] = FichaClinicaBuscaForm(initial={'termo_busca': self.request.GET.get('termo_busca', '')})
        return context


class FichaClinicaDetailView(DetailView):
    model = FichaClinica
    template_name = 'fichas_clinicas/ficha_detail.html'
    context_object_name = 'ficha'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrar fichas por usuário logado
        if self.request.user.is_superuser:
            return queryset  # Superadmins veem todas as fichas
        elif hasattr(self.request.user, 'profile') and self.request.user.profile.is_team_leader:
            # Líderes veem fichas de pacientes da sua clínica
            try:
                clinica = self.request.user.profile.clinica
                if clinica:
                    return queryset.filter(paciente__clinica=clinica)
                else:
                    return queryset.filter(paciente__responsavel=self.request.user)
            except:
                return queryset.filter(paciente__responsavel=self.request.user)
        else:
            # Outros usuários veem apenas fichas de seus pacientes
            return queryset.filter(paciente__responsavel=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessoes'] = self.object.sessoes.all().order_by('-data_sessao')
        context['form_status'] = FichaClinicaStatusForm(instance=self.object)
        return context


@login_required
def ficha_clinica_create(request, paciente_id=None):
    # Se um paciente_id foi fornecido, verificar acesso
    if paciente_id:
        # Verificar se o usuário tem permissão para acessar este paciente
        if request.user.is_superuser:
            paciente = get_object_or_404(Paciente, pk=paciente_id)
        elif hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
            try:
                clinica = request.user.profile.clinica
                if clinica:
                    paciente = get_object_or_404(Paciente, pk=paciente_id, clinica=clinica)
                else:
                    paciente = get_object_or_404(Paciente, pk=paciente_id, responsavel=request.user)
            except:
                paciente = get_object_or_404(Paciente, pk=paciente_id, responsavel=request.user)
        else:
            # Usuário comum só pode criar fichas para seus pacientes
            paciente = get_object_or_404(Paciente, pk=paciente_id, responsavel=request.user)
    
    if request.method == 'POST':
        ficha_form = FichaClinicaForm(request.POST)
        anamnese_form = AnamneseForm(request.POST)
        exame_form = ExameClinicoForm(request.POST)
        diagnostico_form = DiagnosticoForm(request.POST)
        
        # Verificar se é um salvamento parcial
        is_partial_save = 'save_partial' in request.POST
        
        # Para salvamento parcial, verificamos apenas se o formulário principal é válido
        if is_partial_save:
            if ficha_form.is_valid():
                try:
                    # Salvar a ficha clínica
                    ficha = ficha_form.save(commit=False)
                    ficha.criado_por = request.user
                    
                    # Garantir que só crie fichas para pacientes que o usuário tem acesso
                    paciente_selecionado = ficha.paciente
                    if not request.user.is_superuser:
                        if hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
                            # Líder de equipe pode criar para pacientes da clínica
                            if request.user.profile.clinica:
                                if paciente_selecionado.clinica != request.user.profile.clinica:
                                    messages.error(request, 'Você só pode criar fichas para pacientes da sua clínica')
                                    return redirect('dashboard')
                        else:
                            # Usuário comum só pode criar para seus pacientes
                            if paciente_selecionado.responsavel != request.user:
                                messages.error(request, 'Você só pode criar fichas para seus pacientes')
                                return redirect('dashboard')
                    
                    ficha.save()
                    
                    # Salvar modelos relacionados se estiverem válidos
                    if anamnese_form.is_valid():
                        anamnese = anamnese_form.save(commit=False)
                        anamnese.ficha = ficha
                        anamnese.save()
                    
                    if exame_form.is_valid():
                        exame = exame_form.save(commit=False)
                        exame.ficha = ficha
                        exame.save()
                    
                    if diagnostico_form.is_valid():
                        diagnostico = diagnostico_form.save(commit=False)
                        diagnostico.ficha = ficha
                        diagnostico.save()
                    
                    messages.success(request, 'Ficha clínica salva parcialmente com sucesso!')
                    return redirect('fichas_clinicas:ficha_detail', pk=ficha.pk)
                    
                except Exception as e:
                    messages.error(request, f'Erro ao salvar ficha clínica: {str(e)}')
            else:
                messages.error(request, 'Por favor, corrija os erros no formulário principal.')
        # Para salvamento completo, verificamos todos os formulários
        elif all([ficha_form.is_valid(), anamnese_form.is_valid(), 
                exame_form.is_valid(), diagnostico_form.is_valid()]):
            try:
                # Salvar a ficha clínica
                ficha = ficha_form.save(commit=False)
                ficha.criado_por = request.user
                
                # Garantir que só crie fichas para pacientes que o usuário tem acesso
                paciente_selecionado = ficha.paciente
                if not request.user.is_superuser:
                    if hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
                        # Líder de equipe pode criar para pacientes da clínica
                        if request.user.profile.clinica:
                            if paciente_selecionado.clinica != request.user.profile.clinica:
                                messages.error(request, 'Você só pode criar fichas para pacientes da sua clínica')
                                return redirect('dashboard')
                    else:
                        # Usuário comum só pode criar para seus pacientes
                        if paciente_selecionado.responsavel != request.user:
                            messages.error(request, 'Você só pode criar fichas para seus pacientes')
                            return redirect('dashboard')
                
                ficha.save()
                
                # Salvar a anamnese
                anamnese = anamnese_form.save(commit=False)
                anamnese.ficha = ficha
                anamnese.save()
                
                # Salvar o exame clínico
                exame = exame_form.save(commit=False)
                exame.ficha = ficha
                exame.save()
                
                # Salvar o diagnóstico
                diagnostico = diagnostico_form.save(commit=False)
                diagnostico.ficha = ficha
                diagnostico.save()
                
                messages.success(request, 'Ficha clínica criada com sucesso!')
                return redirect('fichas_clinicas:ficha_detail', pk=ficha.pk)
                
            except Exception as e:
                messages.error(request, f'Erro ao criar ficha clínica: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        initial_data = {}
        if paciente_id:
            initial_data['paciente'] = paciente_id
        ficha_form = FichaClinicaForm(initial=initial_data)
        anamnese_form = AnamneseForm()
        exame_form = ExameClinicoForm()
        diagnostico_form = DiagnosticoForm()
    
    return render(request, 'fichas_clinicas/ficha_clinica_form.html', {
        'ficha_form': ficha_form,
        'anamnese_form': anamnese_form,
        'exame_form': exame_form,
        'diagnostico_form': diagnostico_form,
    })


@login_required
def ficha_clinica_update(request, pk):
    # Verificar se o usuário tem acesso à ficha
    if request.user.is_superuser:
        ficha = get_object_or_404(FichaClinica, pk=pk)
    elif hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
        try:
            clinica = request.user.profile.clinica
            if clinica:
                ficha = get_object_or_404(FichaClinica, pk=pk, paciente__clinica=clinica)
            else:
                ficha = get_object_or_404(FichaClinica, pk=pk, paciente__responsavel=request.user)
        except:
            ficha = get_object_or_404(FichaClinica, pk=pk, paciente__responsavel=request.user)
    else:
        # Usuário comum só pode atualizar fichas de seus pacientes
        ficha = get_object_or_404(FichaClinica, pk=pk, paciente__responsavel=request.user)
    
    # Obter ou criar objetos relacionados
    anamnese, _ = Anamnese.objects.get_or_create(ficha=ficha)
    exame_clinico, _ = ExameClinico.objects.get_or_create(ficha=ficha)
    diagnostico, _ = Diagnostico.objects.get_or_create(ficha=ficha)
    
    if request.method == 'POST':
        ficha_form = FichaClinicaForm(request.POST, instance=ficha)
        anamnese_form = AnamneseForm(request.POST, instance=anamnese)
        exame_form = ExameClinicoForm(request.POST, instance=exame_clinico)
        diagnostico_form = DiagnosticoForm(request.POST, instance=diagnostico)
        
        # Verificar se é um salvamento parcial
        is_partial_save = 'save_partial' in request.POST
        
        # Para salvamento parcial, verificamos apenas se o formulário principal é válido
        if is_partial_save:
            if ficha_form.is_valid():
                ficha_nova = ficha_form.save(commit=False)
                
                # Verificar se o paciente selecionado é válido para este usuário
                paciente_selecionado = ficha_nova.paciente
                if not request.user.is_superuser:
                    if hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
                        # Líder de equipe pode atualizar para pacientes da clínica
                        if request.user.profile.clinica:
                            if paciente_selecionado.clinica != request.user.profile.clinica:
                                messages.error(request, 'Você só pode atualizar fichas para pacientes da sua clínica')
                                return redirect('dashboard')
                    else:
                        # Usuário comum só pode atualizar para seus pacientes
                        if paciente_selecionado.responsavel != request.user:
                            messages.error(request, 'Você só pode atualizar fichas para seus pacientes')
                            return redirect('dashboard')
                
                ficha_nova.save()
                
                # Salvar modelos relacionados se estiverem válidos
                if anamnese_form.is_valid():
                    anamnese_form.save()
                
                if exame_form.is_valid():
                    exame_form.save()
                
                if diagnostico_form.is_valid():
                    diagnostico_form.save()
                
                messages.success(request, 'Ficha clínica salva parcialmente com sucesso!')
                return redirect('fichas_clinicas:ficha_detail', pk=ficha.pk)
            else:
                messages.error(request, 'Por favor, corrija os erros no formulário principal.')
        # Para salvamento completo, verificamos todos os formulários
        elif all([ficha_form.is_valid(), anamnese_form.is_valid(), 
                exame_form.is_valid(), diagnostico_form.is_valid()]):
            ficha_nova = ficha_form.save(commit=False)
            
            # Verificar se o paciente selecionado é válido para este usuário
            paciente_selecionado = ficha_nova.paciente
            if not request.user.is_superuser:
                if hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
                    # Líder de equipe pode atualizar para pacientes da clínica
                    if request.user.profile.clinica:
                        if paciente_selecionado.clinica != request.user.profile.clinica:
                            messages.error(request, 'Você só pode atualizar fichas para pacientes da sua clínica')
                            return redirect('dashboard')
                else:
                    # Usuário comum só pode atualizar para seus pacientes
                    if paciente_selecionado.responsavel != request.user:
                        messages.error(request, 'Você só pode atualizar fichas para seus pacientes')
                        return redirect('dashboard')
            
            ficha_nova.save()
            anamnese_form.save()
            exame_form.save()
            diagnostico_form.save()
            
            messages.success(request, 'Ficha clínica atualizada com sucesso!')
            return redirect('fichas_clinicas:ficha_detail', pk=ficha.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        ficha_form = FichaClinicaForm(instance=ficha)
        anamnese_form = AnamneseForm(instance=anamnese)
        exame_form = ExameClinicoForm(instance=exame_clinico)
        diagnostico_form = DiagnosticoForm(instance=diagnostico)
    
    return render(request, 'fichas_clinicas/ficha_clinica_form.html', {
        'ficha_form': ficha_form,
        'anamnese_form': anamnese_form,
        'exame_form': exame_form,
        'diagnostico_form': diagnostico_form,
        'object': ficha,
    })


@login_required
def ficha_clinica_detail(request, pk):
    # Verificar se é superadmin ou líder de equipe
    is_superadmin = request.user.is_superuser
    is_team_leader = False
    try:
        if hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
            is_team_leader = True
    except:
        pass
    
    # Obter a ficha com base no perfil do usuário
    if is_superadmin:
        ficha = get_object_or_404(FichaClinica, pk=pk)
    elif is_team_leader:
        try:
            clinica = request.user.profile.clinica
            if clinica:
                ficha = get_object_or_404(FichaClinica, pk=pk, paciente__clinica=clinica)
            else:
                ficha = get_object_or_404(FichaClinica, pk=pk, paciente__responsavel=request.user)
        except:
            ficha = get_object_or_404(FichaClinica, pk=pk, paciente__responsavel=request.user)
    else:
        # Usuário comum só vê fichas de seus pacientes
        ficha = get_object_or_404(FichaClinica, pk=pk, paciente__responsavel=request.user)
    
    sessoes = ficha.sessoes.all().order_by('-data_sessao')
    
    return render(request, 'fichas_clinicas/ficha_clinica_detail.html', {
        'ficha': ficha,
        'sessoes': sessoes,
    })


@login_required
def ficha_clinica_list(request):
    form = FichaClinicaBuscaForm(request.GET)
    
    # Filtrar fichas por usuário logado
    if request.user.is_superuser:
        fichas = FichaClinica.objects.all().order_by('-data_abertura')  # Superadmins veem todas as fichas
    elif hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
        # Líderes veem fichas de pacientes da sua clínica
        try:
            clinica = request.user.profile.clinica
            if clinica:
                fichas = FichaClinica.objects.filter(paciente__clinica=clinica).order_by('-data_abertura')
            else:
                fichas = FichaClinica.objects.filter(paciente__responsavel=request.user).order_by('-data_abertura')
        except:
            fichas = FichaClinica.objects.filter(paciente__responsavel=request.user).order_by('-data_abertura')
    else:
        # Outros usuários veem apenas fichas de seus pacientes
        fichas = FichaClinica.objects.filter(paciente__responsavel=request.user).order_by('-data_abertura')
    
    if form.is_valid():
        termo_busca = form.cleaned_data.get('termo_busca')
        if termo_busca:
            fichas = fichas.filter(
                Q(paciente__nome__icontains=termo_busca) |
                Q(dente__icontains=termo_busca) |
                Q(queixa_principal__icontains=termo_busca)
            )
    
    return render(request, 'fichas_clinicas/ficha_clinica_list.html', {
        'fichas': fichas,
        'form': form,
    })


class FichaClinicaDeleteView(LoginRequiredMixin, DeleteView):
    model = FichaClinica
    template_name = 'fichas_clinicas/ficha_confirm_delete.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrar fichas por usuário logado
        if self.request.user.is_superuser:
            return queryset  # Superadmins veem todas as fichas
        elif hasattr(self.request.user, 'profile') and self.request.user.profile.is_team_leader:
            # Líderes veem fichas de pacientes da sua clínica
            try:
                clinica = self.request.user.profile.clinica
                if clinica:
                    return queryset.filter(paciente__clinica=clinica)
                else:
                    return queryset.filter(paciente__responsavel=self.request.user)
            except:
                return queryset.filter(paciente__responsavel=self.request.user)
        else:
            # Outros usuários veem apenas fichas de seus pacientes
            return queryset.filter(paciente__responsavel=self.request.user)
    
    def get_success_url(self):
        paciente_id = self.object.paciente.id
        messages.success(self.request, 'Ficha clínica excluída com sucesso!')
        return reverse_lazy('paciente_detalhe', kwargs={'pk': paciente_id})


@login_required
def ficha_clinica_status_update(request, pk):
    # Verificar se o usuário tem acesso à ficha
    if request.user.is_superuser:
        ficha = get_object_or_404(FichaClinica, pk=pk)
    elif hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
        try:
            clinica = request.user.profile.clinica
            if clinica:
                ficha = get_object_or_404(FichaClinica, pk=pk, paciente__clinica=clinica)
            else:
                ficha = get_object_or_404(FichaClinica, pk=pk, paciente__responsavel=request.user)
        except:
            ficha = get_object_or_404(FichaClinica, pk=pk, paciente__responsavel=request.user)
    else:
        # Usuário comum só pode atualizar fichas de seus pacientes
        ficha = get_object_or_404(FichaClinica, pk=pk, paciente__responsavel=request.user)
    
    if request.method == 'POST':
        form = FichaClinicaStatusForm(request.POST, instance=ficha)
        if form.is_valid():
            form.save()
            messages.success(request, 'Status da ficha atualizado com sucesso!')
            return redirect('fichas_clinicas:ficha_detail', pk=ficha.pk)
    else:
        form = FichaClinicaStatusForm(instance=ficha)
    
    return render(request, 'fichas_clinicas/ficha_clinica_status_form.html', {
        'form': form,
        'ficha': ficha,
    })


# Views para Sessões de Atendimento
class SessaoAtendimentoListView(ListView):
    model = SessaoAtendimento
    template_name = 'fichas_clinicas/sessao_list.html'
    context_object_name = 'sessoes'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-data_sessao')
        
        # Filtrar sessões por usuário logado
        if self.request.user.is_superuser:
            pass  # Superadmins veem todas as sessões
        elif hasattr(self.request.user, 'profile') and self.request.user.profile.is_team_leader:
            # Líderes veem sessões de pacientes da sua clínica
            try:
                clinica = self.request.user.profile.clinica
                if clinica:
                    queryset = queryset.filter(ficha__paciente__clinica=clinica)
                else:
                    queryset = queryset.filter(ficha__paciente__responsavel=self.request.user)
            except:
                queryset = queryset.filter(ficha__paciente__responsavel=self.request.user)
        else:
            # Outros usuários veem apenas sessões de seus pacientes
            queryset = queryset.filter(ficha__paciente__responsavel=self.request.user)
        
        termo_busca = self.request.GET.get('termo_busca', '')
        
        if termo_busca:
            queryset = queryset.filter(
                Q(ficha__paciente__nome__icontains=termo_busca) | 
                Q(ficha__dente__icontains=termo_busca) | 
                Q(procedimentos__icontains=termo_busca)
            )
        
        return queryset

@login_required
def sessao_create(request, ficha_pk):
    # Verificar se o usuário tem acesso à ficha
    if request.user.is_superuser:
        ficha = get_object_or_404(FichaClinica, pk=ficha_pk)
    elif hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
        try:
            clinica = request.user.profile.clinica
            if clinica:
                ficha = get_object_or_404(FichaClinica, pk=ficha_pk, paciente__clinica=clinica)
            else:
                ficha = get_object_or_404(FichaClinica, pk=ficha_pk, paciente__responsavel=request.user)
        except:
            ficha = get_object_or_404(FichaClinica, pk=ficha_pk, paciente__responsavel=request.user)
    else:
        # Usuário comum só pode criar sessões para fichas de seus pacientes
        ficha = get_object_or_404(FichaClinica, pk=ficha_pk, paciente__responsavel=request.user)
    
    if request.method == 'POST':
        form = SessaoAtendimentoForm(request.POST)
        if form.is_valid():
            sessao = form.save(commit=False)
            sessao.ficha = ficha
            sessao.realizado_por = request.user
            sessao.save()
            
            messages.success(request, 'Sessão registrada com sucesso!')
            return redirect('fichas_clinicas:ficha_detail', pk=ficha.pk)
    else:
        form = SessaoAtendimentoForm()
    
    return render(request, 'fichas_clinicas/sessao_form.html', {
        'form': form,
        'ficha_id': ficha.pk,
    })


@login_required
def sessao_update(request, pk):
    # Verificar se o usuário tem acesso à sessão
    if request.user.is_superuser:
        sessao = get_object_or_404(SessaoAtendimento, pk=pk)
    elif hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
        try:
            clinica = request.user.profile.clinica
            if clinica:
                sessao = get_object_or_404(SessaoAtendimento, pk=pk, ficha__paciente__clinica=clinica)
            else:
                sessao = get_object_or_404(SessaoAtendimento, pk=pk, ficha__paciente__responsavel=request.user)
        except:
            sessao = get_object_or_404(SessaoAtendimento, pk=pk, ficha__paciente__responsavel=request.user)
    else:
        # Usuário comum só pode atualizar sessões para fichas de seus pacientes
        sessao = get_object_or_404(SessaoAtendimento, pk=pk, ficha__paciente__responsavel=request.user)
    
    if request.method == 'POST':
        form = SessaoAtendimentoForm(request.POST, instance=sessao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sessão atualizada com sucesso!')
            return redirect('fichas_clinicas:ficha_detail', pk=sessao.ficha.pk)
    else:
        form = SessaoAtendimentoForm(instance=sessao)
    
    return render(request, 'fichas_clinicas/sessao_form.html', {
        'form': form,
        'ficha_id': sessao.ficha.pk,
    })


class SessaoAtendimentoDeleteView(LoginRequiredMixin, DeleteView):
    model = SessaoAtendimento
    template_name = 'fichas_clinicas/sessao_confirm_delete.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrar sessões por usuário logado
        if self.request.user.is_superuser:
            return queryset  # Superadmins veem todas as sessões
        elif hasattr(self.request.user, 'profile') and self.request.user.profile.is_team_leader:
            # Líderes veem sessões de pacientes da sua clínica
            try:
                clinica = self.request.user.profile.clinica
                if clinica:
                    return queryset.filter(ficha__paciente__clinica=clinica)
                else:
                    return queryset.filter(ficha__paciente__responsavel=self.request.user)
            except:
                return queryset.filter(ficha__paciente__responsavel=self.request.user)
        else:
            # Outros usuários veem apenas sessões de seus pacientes
            return queryset.filter(ficha__paciente__responsavel=self.request.user)
    
    def get_success_url(self):
        ficha_id = self.object.ficha.id
        messages.success(self.request, 'Sessão de atendimento excluída com sucesso!')
        return reverse_lazy('fichas_clinicas:ficha_detail', kwargs={'pk': ficha_id})


class SessaoAtendimentoDetailView(DetailView):
    model = SessaoAtendimento
    template_name = 'fichas_clinicas/sessao_detail.html'
    context_object_name = 'sessao'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrar sessões por usuário logado
        if self.request.user.is_superuser:
            return queryset  # Superadmins veem todas as sessões
        elif hasattr(self.request.user, 'profile') and self.request.user.profile.is_team_leader:
            # Líderes veem sessões de pacientes da sua clínica
            try:
                clinica = self.request.user.profile.clinica
                if clinica:
                    return queryset.filter(ficha__paciente__clinica=clinica)
                else:
                    return queryset.filter(ficha__paciente__responsavel=self.request.user)
            except:
                return queryset.filter(ficha__paciente__responsavel=self.request.user)
        else:
            # Outros usuários veem apenas sessões de seus pacientes
            return queryset.filter(ficha__paciente__responsavel=self.request.user)


# Views para listar fichas por paciente
@login_required
def listar_fichas_paciente(request, paciente_id):
    # Verificar se é superadmin ou líder de equipe
    is_superadmin = request.user.is_superuser
    is_team_leader = False
    try:
        if hasattr(request.user, 'profile') and request.user.profile.is_team_leader:
            is_team_leader = True
    except:
        pass
    
    # Obter o paciente com base no perfil do usuário
    if is_superadmin:
        paciente = get_object_or_404(Paciente, pk=paciente_id)
    elif is_team_leader:
        try:
            clinica = request.user.profile.clinica
            if clinica:
                paciente = get_object_or_404(Paciente, pk=paciente_id, clinica=clinica)
            else:
                paciente = get_object_or_404(Paciente, pk=paciente_id, responsavel=request.user)
        except:
            paciente = get_object_or_404(Paciente, pk=paciente_id, responsavel=request.user)
    else:
        # Usuário comum só vê pacientes que é responsável
        paciente = get_object_or_404(Paciente, pk=paciente_id, responsavel=request.user)
    
    fichas = FichaClinica.objects.filter(paciente=paciente).order_by('-data_abertura')
    
    context = {
        'paciente': paciente,
        'fichas': fichas,
    }
    
    return render(request, 'fichas_clinicas/fichas_paciente.html', context)