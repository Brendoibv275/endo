from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class FuncaoUsuario(models.Model):
    nome = models.CharField('Nome da Função', max_length=100)
    descricao = models.TextField('Descrição', blank=True, null=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Função de Usuário'
        verbose_name_plural = 'Funções de Usuários'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_team_leader = models.BooleanField(default=False)
    funcao = models.ForeignKey(FuncaoUsuario, on_delete=models.SET_NULL, null=True)
    clinica = models.ForeignKey('Clinica', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.funcao.nome if self.funcao else 'Sem função'}"

    def save(self, *args, **kwargs):
        # Se for líder de equipe, garante que o usuário seja staff e superuser
        if self.is_team_leader:
            self.user.is_staff = True
            self.user.is_superuser = True
            self.user.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

class TeamMember(models.Model):
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_members')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')
    created_at = models.DateTimeField('Data de Adição', auto_now_add=True)

    class Meta:
        verbose_name = 'Membro da Equipe'
        verbose_name_plural = 'Membros da Equipe'
        unique_together = ('team_leader', 'member')

    def __str__(self):
        return f"{self.member.username} em equipe de {self.team_leader.username}"

class Paciente(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )
    
    nome = models.CharField('Nome completo', max_length=100)
    data_nascimento = models.DateField('Data de nascimento')
    sexo = models.CharField('Sexo', max_length=1, choices=SEXO_CHOICES)
    cpf = models.CharField('CPF', max_length=14, unique=True, help_text='Formato: 000.000.000-00')
    telefone = models.CharField('Telefone', max_length=15, help_text='Formato: (00) 00000-0000')
    email = models.EmailField('E-mail', blank=True, null=True)
    endereco = models.CharField('Endereço', max_length=200)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2)
    cep = models.CharField('CEP', max_length=9, help_text='Formato: 00000-000')
    foto = models.ImageField('Foto do Paciente', upload_to='pacientes/fotos/', blank=True, null=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    data_cadastro = models.DateTimeField('Data de cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última atualização', auto_now=True)
    ativo = models.BooleanField('Ativo', default=True)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name='Responsável')
    clinica = models.ForeignKey('Clinica', on_delete=models.CASCADE, null=True, blank=True, related_name='pacientes', verbose_name='Clínica')
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('paciente_detalhe', kwargs={'pk': self.pk})
    
    def idade(self):
        from datetime import date
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['nome']

class Clinica(models.Model):
    nome = models.CharField('Nome da Clínica', max_length=100)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    endereco = models.CharField('Endereço', max_length=200)
    telefone = models.CharField('Telefone', max_length=15)
    email = models.EmailField('E-mail')
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinicas_geridas')
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Clínica'
        verbose_name_plural = 'Clínicas'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()