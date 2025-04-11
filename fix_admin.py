import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odonto_endo.settings')
django.setup()

from django.contrib.auth.models import User
from pacientes.models import UserProfile, FuncaoUsuario

def fix_admin_permissions():
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
        print(f'Atualizado perfil de {profile.user.username}')

    # Criar superusuário padrão se não existir
    if not User.objects.filter(username='brendo12').exists():
        user = User.objects.create_superuser(
            username='brendo12',
            password='brendo1293',
            email='admin@example.com'
        )
        UserProfile.objects.create(
            user=user,
            is_team_leader=True,
            funcao=funcao_admin
        )
        print('Superusuário brendo12 criado com sucesso!')
    
    print('Permissões de administrador corrigidas com sucesso!')

if __name__ == '__main__':
    fix_admin_permissions() 