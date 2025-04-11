from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'pacientes'

urlpatterns = [
    # URLs de autenticação
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # URLs de pacientes
    path('', views.PacienteListView.as_view(), name='paciente_lista'),
    path('paciente/<int:pk>/', views.PacienteDetailView.as_view(), name='paciente_detalhe'),
    path('paciente/novo/', views.PacienteCreateView.as_view(), name='paciente_novo'),
    path('paciente/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente_editar'),
    path('paciente/<int:pk>/excluir/', views.PacienteDeleteView.as_view(), name='paciente_excluir'),
    
    # URLs de equipe
    path('equipe/', views.team_management, name='team_management'),
    path('equipe/adicionar/', views.add_team_member, name='add_team_member'),
    path('equipe/<int:member_id>/remover/', views.remove_team_member, name='remove_team_member'),
    
    # URLs de clínica
    path('clinica/', views.clinica_management, name='clinica_management'),
    path('clinica/adicionar-usuario/', views.add_clinica_user, name='add_clinica_user'),
    path('clinica/remover/<int:user_id>/', views.remove_clinica_user, name='remove_clinica_user'),
]