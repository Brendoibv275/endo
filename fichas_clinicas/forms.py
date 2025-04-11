from django import forms
from .models import FichaClinica, SessaoAtendimento, Anamnese, ExameClinico, Diagnostico
from pacientes.models import Paciente

class AnamneseForm(forms.ModelForm):
    class Meta:
        model = Anamnese
        fields = '__all__'
        widgets = {
            'outras_condicoes': forms.Textarea(attrs={'rows': 3}),
            'historia_dental': forms.Textarea(attrs={'rows': 3}),
            'exacerbada_outro': forms.TextInput(attrs={'placeholder': 'Especifique outro fator'}),
            'aliviada_outro': forms.TextInput(attrs={'placeholder': 'Especifique outro fator'}),
        }

class ExameClinicoForm(forms.ModelForm):
    class Meta:
        model = ExameClinico
        fields = '__all__'

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = '__all__'
        widgets = {
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
            'acidentes_operatorios': forms.Textarea(attrs={'rows': 3}),
            'pos_tratamento': forms.Textarea(attrs={'rows': 3}),
        }

class FichaClinicaForm(forms.ModelForm):
    class Meta:
        model = FichaClinica
        fields = ['paciente', 'dente', 'queixa_principal', 'status', 'data_abertura']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'dente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 11, 21, etc.'}),
            'queixa_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'data_abertura': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class SessaoAtendimentoForm(forms.ModelForm):
    class Meta:
        model = SessaoAtendimento
        fields = '__all__'
        exclude = ['ficha']
        widgets = {
            'procedimentos': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            'materiais': forms.Textarea(attrs={'rows': 3}),
            'data_sessao': forms.DateInput(attrs={'type': 'date'}),
        }

class FichaClinicaBuscaForm(forms.Form):
    termo_busca = forms.CharField(
        label='Buscar Ficha',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por paciente, dente ou diagnóstico...'})
    )

class FichaClinicaStatusForm(forms.ModelForm):
    class Meta:
        model = FichaClinica
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }