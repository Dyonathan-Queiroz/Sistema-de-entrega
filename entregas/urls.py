from django.urls import path
from . import views

urlpatterns = [
    # --- AUTENTICAÇÃO E INÍCIO ---
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- PAINEL DO OPERADOR E CLIENTES ---
    path('painel-operador/', views.painel_operador, name='painel_operador'),
    path('cliente/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/excluir/<int:pk>/', views.excluir_cliente, name='excluir_cliente'),

    # --- LANÇAMENTO DE ENTREGAS ---
    # Nota: O nome da URL deve bater com o que está no botão do seu HTML
    path('cliente/<int:cliente_id>/nova-entrega/', views.criar_entrega_cliente, name='criar_entrega_cliente'),

    # --- GESTÃO DE VEÍCULOS ---
    path('veiculos/novo/', views.cadastro_veiculo, name='cadastro_veiculo'),
    path('veiculo/editar/<int:pk>/', views.editar_veiculo, name='editar_veiculo'),
    path('veiculo/excluir/<int:pk>/', views.excluir_veiculo, name='excluir_veiculo'),

    # --- GESTÃO DE FILIAIS ---
    path('filiais/', views.gerenciar_filiais, name='gerenciar_filiais'),
    path('filiais/editar/<int:pk>/', views.editar_filial, name='editar_filial'),
    path('filiais/excluir/<int:pk>/', views.excluir_filial, name='excluir_filial'),

    # --- GESTÃO DE EQUIPE (USUÁRIOS) ---
    path('equipe/', views.gerenciar_equipe, name='gerenciar_equipe'),
    path('equipe/editar/<int:pk>/', views.editar_equipe, name='editar_equipe'),
    path('equipe/excluir/<int:pk>/', views.excluir_equipe, name='excluir_equipe'),
]