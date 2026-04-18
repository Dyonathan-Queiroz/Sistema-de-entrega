from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Entrega, Veiculo, Filial, Usuario, Cliente
from .forms import VeiculoForm, FilialForm, UsuarioForm, ClienteForm, LancarEntregaForm
from django.utils import timezone
from django.db.models import Q


# --- 1. AUTENTICAÇÃO E LOGIN ---

def login_view(request):
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

def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu do sistema.")
    return redirect('login')

# --- 2. DASHBOARD (O MAESTRO) ---

@login_required
def dashboard(request):
    user = request.user
    
    # 1. REDIRECIONAMENTOS DIRETOS
    if user.perfil == 'operador':
        return redirect('painel_operador')
    
    if user.perfil == 'entregador':
        return redirect('painel_entregador')

    # 2. LÓGICA DE DADOS PARA GESTOR
    # Primeiro, calculamos as entregas reportadas
    entregas_reportadas = Entrega.objects.filter(
        status='pendente'
    ).exclude(observacao_entrega__isnull=True).exclude(observacao_entrega='')

    context = {
        'perfil': user.perfil,
        'nome_usuario': user.get_full_name() or user.username,
        # Estatísticas gerais
        'total_entregas': Entrega.objects.count(),
        'total_clientes': Cliente.objects.count(),
        'veiculos_disponiveis': Veiculo.objects.filter(status='disponivel').count(),
        
        # Monitoramento em tempo real
        'entregas_pendentes': Entrega.objects.filter(status='pendente').count(),
        'entregas_em_rota': Entrega.objects.filter(status='em_rota').count(),
        'entregas_finalizadas': Entrega.objects.filter(status='entregue').count(),
        
        # Adicionamos a lista de reportadas ao contexto para poder usar no template
        'entregas_reportadas': entregas_reportadas,
        
        # Dados para listagem
        'clientes': Cliente.objects.all().order_by('-id'),
        'form_cliente': ClienteForm(),
    }

    # Se for gestor, renderiza o painel dele com o contexto completo
    if user.perfil == 'gestor':
        return render(request, 'entregas/dashboard_gestor.html', context)
    
    # Fallback de segurança
    return redirect('painel_operador')


# --- 3. PAINEL DO OPERADOR E CLIENTES (CRUD) ---

@login_required
def painel_operador(request):
    # 1. Verificação de Perfil
    if request.user.perfil not in ['operador', 'gestor']:
        messages.error(request, "Acesso negado.")
        return redirect('dashboard')
    
    # Pega o termo digitado na busca #
    query = request.GET.get('q')
    
    if query:
        # Filtra por nome ou documento (CPF/CNPJ)
        clientes = Cliente.objects.filter(
            Q(nome__icontains=query) | Q(documento__icontains=query)
        ).order_by('-id')
    else:
        clientes = Cliente.objects.all().order_by('-id')
    
    # Lógica de salvamento continua igual...
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST)
        if form_cliente.is_valid():
            form_cliente.save()
            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect('painel_operador')
        else:
            form_cliente = ClienteForm(request.POST)
    else:
        form_cliente = ClienteForm()

    return render(request, 'entregas/dashboard_operador.html', {
        'clientes': clientes, 
        'form_cliente': form_cliente,
        'query': query # Passamos de volta para o HTML para manter o texto na caixa
    })

    # 2. Busca de dados
    clientes = Cliente.objects.all().order_by('-id')
    
    
    # 3. Lógica de Salvamento (POST)
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST)
        if form_cliente.is_valid():
            form_cliente.save()
            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect('painel_operador')
        else:
            # Se houver erro, NÃO damos redirect. 
            # Renderizamos a página novamente para mostrar os erros nos campos.
            messages.error(request, "Erro ao cadastrar cliente. Verifique os campos em vermelho.")
    else:
        # Método GET: Formulário vazio
        form_cliente = ClienteForm()

    return render(request, 'entregas/dashboard_operador.html', {
        'clientes': clientes, 
        'form_cliente': form_cliente
    })

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.info(request, "Cliente atualizado com sucesso.")
            return redirect('painel_operador')
        else:
            messages.error(request, "Erro ao atualizar. Verifique os dados.")
    else:
        form = ClienteForm(instance=cliente)
        
    return render(request, 'entregas/editar_cliente.html', {
        'form': form, 
        'cliente': cliente
    })

@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    messages.warning(request, "Cliente removido do sistema.")
    return redirect('painel_operador')

# --- 4. GESTÃO DE VEÍCULOS ---

@login_required
def cadastro_veiculo(request):
    if request.user.perfil != 'gestor':
        return redirect('dashboard')
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Veículo cadastrado!")
            return redirect('cadastro_veiculo')
    else:
        form = VeiculoForm()
    veiculos = Veiculo.objects.all()
    return render(request, 'entregas/cadastro_veiculo.html', {'form': form, 'veiculos': veiculos})

@login_required
def editar_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('cadastro_veiculo')
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, 'entregas/editar_veiculo.html', {'form': form})

@login_required
def excluir_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    veiculo.delete()
    return redirect('cadastro_veiculo')

# --- 5. GESTÃO DE FILIAIS ---

@login_required
def gerenciar_filiais(request):
    if request.user.perfil != 'gestor':
        return redirect('dashboard')
    filiais = Filial.objects.all()
    if request.method == 'POST':
        form = FilialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_filiais')
    else:
        form = FilialForm()
    return render(request, 'entregas/gerenciar_filiais.html', {'filiais': filiais, 'form': form})

@login_required
def editar_filial(request, pk):
    filial = get_object_or_404(Filial, pk=pk)
    if request.method == 'POST':
        form = FilialForm(request.POST, instance=filial)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_filiais')
    else:
        form = FilialForm(instance=filial)
    return render(request, 'entregas/editar_filial.html', {'form': form})

@login_required
def excluir_filial(request, pk):
    filial = get_object_or_404(Filial, pk=pk)
    filial.delete()
    return redirect('gerenciar_filiais')

# --- 6. GESTÃO DE EQUIPE ---

@login_required
def gerenciar_equipe(request):
    if request.user.perfil != 'gestor':
        return redirect('dashboard')
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_equipe')
    else:
        form = UsuarioForm()
    return render(request, 'entregas/gerenciar_equipe.html', {'equipe': usuarios, 'form': form})

@login_required
def editar_equipe(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_equipe')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'entregas/editar_equipe.html', {'form': form})

@login_required
def excluir_equipe(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.delete()
    return redirect('gerenciar_equipe')

# --- 7. LANÇAMENTO DE ENTREGAS ---

@login_required
def criar_entrega_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == "POST":
        form = LancarEntregaForm(request.POST)
        if form.is_valid():
            try:
                entrega = form.save(commit=False)
                
                # Preenchimento automático baseado no cadastro do cliente
                entrega.cliente = cliente
                entrega.operador = request.user
                entrega.status = ''
                entrega.valor = 0
                
                # Lógica de Filial: Prioriza a do cliente, se não tiver, pega a primeira do banco
                if cliente.filial:
                    entrega.filial_origem = cliente.filial
                else:
                    from .models import Filial
                    entrega.filial_origem = Filial.objects.first()
                
                entrega.save()
                
                messages.success(request, f"Entrega para {cliente.nome} postada com sucesso!")
                return redirect('painel_operador')
                
            except Exception as e:
                print(f"ERRO AO SALVAR: {e}")
                messages.error(request, f"Erro técnico: {e}")
        else:
            print(form.errors)
    else:
        # Preenche com os dados atuais do cliente
        dados_iniciais = {
            'rua': cliente.rua,
            'numero': cliente.numero,
            'bairro': cliente.bairro,
            'ponto_referencia': cliente.ponto_referencia,
            'observacao_entrega': cliente.observacoes_fixas,
        }
        form = LancarEntregaForm(initial=dados_iniciais)

    return render(request, 'entregas/lancar_entrega.html', {'form': form, 'cliente': cliente})

# -- referente a entregador ---
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def painel_entregador(request):
    # 1. Busca entregas em rota para o entregador logado
    entregas_em_rota = Entrega.objects.filter(entregador=request.user, status='em_rota')
    
    # 2. Busca entregas pendentes (que não possuem observação/problema)
    # Usamos Q para garantir: (observacao é nula OU está vazia)
    entregas_pendentes = Entrega.objects.filter(status='pendente').filter(
        Q(observacao_entrega__isnull=True) | Q(observacao_entrega='')
    )
    
    # 3. Retorno apenas com as listas de entregas
    return render(request, 'entregas/painel_entregador.html', {
        'entregas_em_rota': entregas_em_rota,
        'entregas_pendentes': entregas_pendentes,
    })
    
# --- FUNÇÕES PARA O ENTREGADOR ---

@login_required
def aceitar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id)
    if entrega.status == 'pendente':
        entrega.entregador = request.user
        entrega.status = 'em_rota'
        entrega.data_saida = timezone.now()
        entrega.save()
        messages.success(request, "Boa! Entrega aceita.")
    return redirect('painel_entregador')

@login_required
def finalizar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id, entregador=request.user)
    if entrega.status == 'em_rota':
        entrega.status = 'entregue'
        entrega.data_finalizacao = timezone.now() # Certifique-se de ter esse campo no models
        entrega.save()
        messages.success(request, "Entrega finalizada com sucesso!")
    return redirect('painel_entregador')

@login_required
def detalhes_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id)
    
    # Monta o endereço para o Google Maps
    endereco_completo = f"{entrega.rua}, {entrega.numero}, {entrega.bairro}, Boa Vista"
    import urllib.parse
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(endereco_completo)}"
    
    return render(request, 'entregas/detalhes_entrega.html', {
        'entrega': entrega,
        'google_maps_url': google_maps_url
    })




@login_required
def reportar_pendencia(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id)
    if request.method == 'POST':
        observacao = request.POST.get('observacao')
        entrega.status = 'pendente'  # Volta para a fila
        entrega.entregador = None    # Libera a entrega
        entrega.observacao_entrega = f"Problema: {observacao}" # Registra o erro
        entrega.save()
        messages.warning(request, "Entrega reportada como pendente.")
        return redirect('painel_entregador')
    return redirect('detalhes_entrega', entrega_id=entrega_id)

@login_required
def reliberar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id)
    # Limpa os dados do problema para a entrega ficar "nova" na fila
    entrega.entregador = None
    entrega.observacao_entrega = None 
    entrega.status = 'pendente'
    entrega.save()
    messages.success(request, "Entrega re-liberada para a fila!")
    return redirect('dashboard')