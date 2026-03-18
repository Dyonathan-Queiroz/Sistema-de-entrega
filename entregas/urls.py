from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'), # Página inicial após login
    path('veiculos/novo/', views.cadastro_veiculo, name='cadastro_veiculo'), # Cadastro de veiculos
    path('veiculo/excluir/<int:pk>/', views.excluir_veiculo, name='excluir_veiculo'), # Excluir veiculos
    path('veiculo/editar/<int:pk>/', views.editar_veiculo, name='editar_veiculo'), # Editar Veiculos
    path('filiais/', views.gerenciar_filiais, name='gerenciar_filiais'), # Cadastrar filial
    path('filiais/excluir/<int:pk>/', views.excluir_filial, name='excluir_filial'), # Excluir filial
    path('filiais/editar/<int:pk>/', views.editar_filial, name='editar_filial'), # Editar Filial
]