from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pacientes.models import UserProfile, FuncaoUsuario

class Command(BaseCommand):
    help = 'Corrige as permissões dos usuários administradores'

    def handle(self, *args, **kwargs):
        # Criar função de administrador se não existir
        funcao_admin, _ = FuncaoUsuario.objects.get_or_create(nome='Administrador')
        
        # Atualizar todos os perfis de administradores
        admin_profiles = UserProfile.objects.filter(is_team_leader=True)
        for profile in admin_profiles:
            profile.user.is_staff = True
            profile.user.is_superuser = True
            profile.user.save()
            profile.funcao = funcao_admin
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'Atualizado perfil de {profile.user.username}'))
        
        self.stdout.write(self.style.SUCCESS('Permissões de administrador corrigidas com sucesso!')) 