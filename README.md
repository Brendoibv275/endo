# Sistema de Gerenciamento Odontológico - Endodontia

Um sistema web desenvolvido em Django para gerenciamento de pacientes e tratamentos odontológicos, com foco em endodontia.

## Funcionalidades Atuais

- Gerenciamento de Pacientes:
  - Cadastro de pacientes com informações pessoais e de contato
  - Listagem e busca de pacientes
  - Visualização detalhada do perfil do paciente
  - Edição e exclusão de pacientes

## Requisitos

- Python 3.8+
- Django 4.2+
- Outras dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
5. Execute as migrações:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Crie um superusuário:
   ```
   python manage.py createsuperuser
   ```
7. Inicie o servidor:
   ```
   python manage.py runserver
   ```
8. Acesse o sistema em `http://127.0.0.1:8000`

## Próximos Passos

- Implementação de módulo específico para tratamentos endodônticos
- Sistema de agendamento de consultas
- Histórico de tratamentos
- Relatórios e estatísticas
- Integração com sistema de imagens radiográficas

## Licença

Este projeto está licenciado sob a licença MIT.