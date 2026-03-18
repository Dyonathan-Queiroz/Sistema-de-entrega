from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Entrega # Importe seus modelos conforme precisar
from .forms import VeiculoForm


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

@login_required
def cadastro_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            if not veiculo.filial and hasattr(request.user, 'filial'):
                veiculo.filial = request.user.filial
            veiculo.save()
            messages.success(request, f"Veículo {veiculo.placa} cadastrado!")
            return redirect('cadastro_veiculo') # Recarrega a página para limpar o form
    else:
        form = VeiculoForm()
    
    # Buscamos todos os veículos para a tabela
    veiculos = Veiculo.objects.all().order_by('-id')
    
    return render(request, 'entregas/cadastro_veiculo.html', {
        'form': form,
        'veiculos': veiculos
    })

@login_required
def excluir_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    placa = veiculo.placa
    veiculo.delete()
    messages.warning(request, f"Veículo {placa} removido com sucesso!")
    return redirect('cadastro_veiculo')

@login_required
def editar_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    
    if request.method == 'POST':
        # Aqui o 'instance=veiculo' faz o Django entender que é um UPDATE, não um novo INSERT
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Veículo {veiculo.placa} atualizado com sucesso!")
            return redirect('cadastro_veiculo')
    else:
        form = VeiculoForm(instance=veiculo)
    
    return render(request, 'entregas/editar_veiculo.html', {'form': form, 'veiculo': veiculo})