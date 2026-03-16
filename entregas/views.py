from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Entrega # Importe seus modelos conforme precisar

def login_view(request):
    # Se o usuário já estiver logado, manda direto para o dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        usuario_post = request.POST.get('username')
        senha_post = request.POST.get('password')

        user = authenticate(request, username=usuario_post, password=senha_post)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return render(request, 'entregas/login.html')

    return render(request, 'entregas/login.html')

@login_required
def dashboard(request):
    """
    View principal que direciona o usuário baseada no perfil
    """
    user = request.user
    
    # Exemplo de lógica de contexto por perfil
    context = {
        'perfil': user.perfil,
        'nome_usuario': user.get_full_name() or user.username,
    }

    # Redirecionamento ou renderização baseada no perfil do seu models.py
    if user.perfil == 'gestor':
        # Aqui você pode buscar dados específicos para o gestor
        return render(request, 'entregas/dashboard_gestor.html', context)
    
    elif user.perfil == 'entregador':
        # Busca apenas as entregas do próprio entregador
        context['minhas_entregas'] = Entrega.objects.filter(entregador=user, status='em_rota')
        return render(request, 'entregas/dashboard_entregador.html', context)
    
    # Caso seja operador ou outro
    return render(request, 'entregas/dashboard_operador.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu do sistema.")
    return redirect('login')

    from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Entrega, Veiculo, Cliente

@login_required
def dashboard(request):
    user = request.user
    
    # Buscando dados reais do banco para os Cards
    total_entregas = Entrega.objects.count()
    entregas_pendentes = Entrega.objects.filter(status='pendente').count()
    veiculos_disponiveis = Veiculo.objects.filter(status='disponivel').count()
    total_clientes = Cliente.objects.count()

    context = {
        'perfil': user.perfil,
        'nome_usuario': user.get_full_name() or user.username,
        # Passando os números para o HTML
        'total_entregas': total_entregas,
        'entregas_pendentes': entregas_pendentes,
        'veiculos_disponiveis': veiculos_disponiveis,
        'total_clientes': total_clientes,
    }

    if user.perfil == 'gestor':
        return render(request, 'entregas/dashboard_gestor.html', context)
    elif user.perfil == 'entregador':
        context['minhas_entregas'] = Entrega.objects.filter(entregador=user, status='em_rota')
        return render(request, 'entregas/dashboard_entregador.html', context)
    
    return render(request, 'entregas/dashboard_operador.html', context)