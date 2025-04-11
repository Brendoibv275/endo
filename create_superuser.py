import os
import django
from django.contrib.auth import get_user_model

# Configurar as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odonto_endo.settings')
django.setup()

def create_superuser():
    User = get_user_model()
    
    # Verificar se o usuário já existe
    if not User.objects.filter(username='brendo93').exists():
        # Criar o superusuário
        User.objects.create_superuser(
            username='brendo93',
            email='denkulol@gmail.com',
            password='brendo0412'
        )
        print('Superusuário criado com sucesso!')
        print('Username: brendo93')
        print('Password: brendo0412')
    else:
        print('O usuário brendo12 já existe!')

if __name__ == '__main__':
    create_superuser()