from django.urls import path
from . import views

app_name = 'fichas_clinicas'

urlpatterns = [
    # URLs para Fichas Clínicas
    path('', views.ficha_clinica_list, name='list'),
    path('ficha/<int:pk>/', views.ficha_clinica_detail, name='ficha_detail'),
    path('ficha/nova/', views.ficha_clinica_create, name='create'),
    path('ficha/nova/', views.ficha_clinica_create, name='ficha_nova'),
    path('ficha/nova/paciente/<int:paciente_id>/', views.ficha_clinica_create, name='ficha_nova_paciente'),
    path('ficha/<int:pk>/editar/', views.ficha_clinica_update, name='update'),
    path('ficha/<int:pk>/editar/', views.ficha_clinica_update, name='ficha_editar'),
    path('ficha/<int:pk>/excluir/', views.FichaClinicaDeleteView.as_view(), name='delete'),
    path('ficha/<int:pk>/status/', views.ficha_clinica_status_update, name='status_update'),
    
    # URLs para Sessões de Atendimento
    path('sessoes/', views.SessaoAtendimentoListView.as_view(), name='sessao_lista'),
    path('<int:ficha_pk>/sessao/nova/', views.sessao_create, name='sessao_create'),
    path('<int:ficha_pk>/sessao/nova/', views.sessao_create, name='sessao_nova'),
    path('sessao/<int:pk>/', views.SessaoAtendimentoDetailView.as_view(), name='sessao_detalhe'),
    path('sessao/<int:pk>/editar/', views.sessao_update, name='sessao_update'),
    path('sessao/<int:pk>/excluir/', views.SessaoAtendimentoDeleteView.as_view(), name='sessao_excluir'),
    
    # URLs para listar fichas por paciente
    path('paciente/<int:paciente_id>/fichas/', views.listar_fichas_paciente, name='fichas_paciente'),
]