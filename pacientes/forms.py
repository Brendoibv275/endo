from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Paciente, TeamMember, FuncaoUsuario

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'sexo', 'cpf', 'telefone', 'email', 
                  'endereco', 'cidade', 'estado', 'cep', 'foto', 'observacoes', 'responsavel']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
        }

class PacienteBuscaForm(forms.Form):
    termo_busca = forms.CharField(
        label='Buscar paciente', 
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nome, CPF ou telefone'})
    )

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    is_admin = forms.BooleanField(
        required=False,
        label='Sou administrador',
        help_text='Marque esta opção se você será o administrador do sistema'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_admin')
        help_texts = {
            'username': 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.',
            'password1': 'Sua senha deve conter pelo menos 8 caracteres e não pode ser muito comum.',
            'password2': 'Digite a mesma senha novamente para verificação.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = (
            'Sua senha deve conter pelo menos 8 caracteres e não pode ser muito comum.'
        )
        self.fields['password2'].help_text = 'Digite a mesma senha novamente para verificação.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Criar perfil do usuário
            from .models import UserProfile, FuncaoUsuario
            
            # Obter ou criar a função de administrador
            funcao_nome = 'Administrador' if self.cleaned_data['is_admin'] else 'Funcionário'
            funcao, _ = FuncaoUsuario.objects.get_or_create(nome=funcao_nome)
            
            profile = UserProfile.objects.create(
                user=user,
                is_team_leader=self.cleaned_data['is_admin'],
                funcao=funcao
            )
        
        return user

class TeamMemberForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = TeamMember
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            raise forms.ValidationError('Usuário com este email não encontrado.')
    
    def save(self, commit=True):
        member = super().save(commit=False)
        member.member = self.cleaned_data['email']
        if commit:
            member.save()
        return member

class ClinicaUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
        help_text='A senha deve conter pelo menos 8 caracteres, incluindo letras e números.'
    )
    password2 = forms.CharField(
        label='Confirmação de senha',
        widget=forms.PasswordInput,
        help_text='Digite a mesma senha novamente para confirmação.'
    )
    funcao = forms.ModelChoiceField(
        queryset=FuncaoUsuario.objects.all(),
        label='Função',
        help_text='Selecione a função do usuário na clínica.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'funcao']
        help_texts = {
            'username': 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.',
            'email': 'Digite um endereço de email válido.',
            'first_name': 'Digite o nome do usuário.',
            'last_name': 'Digite o sobrenome do usuário.',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')

        if password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, funcao=self.cleaned_data['funcao'])
        return user