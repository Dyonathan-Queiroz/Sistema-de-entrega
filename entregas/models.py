from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Cadastro de Filiais (Sua estrutura de rede/unidades)
class Filial(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Filiais"

    def __str__(self):
        return self.nome

# 2. Usuário Customizado (Substitui o User padrão do Django)
class Usuario(AbstractUser):
    PERFIL_CHOICES = (
        ('gestor', 'Gestor'),
        ('operador', 'Operador'),
        ('entregador', 'Entregador'),
    )
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='gestor')
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    veiculo = models.ForeignKey('Veiculo', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_perfil_display()})"

# 3. Cadastro de Veículos (Controle de frota e manutenção)
class Veiculo(models.Model):
    STATUS_CHOICES = (
        ('disponivel', 'Disponível'),
        ('em_rota', 'Em Rota'),
        ('manutencao', 'Manutenção'),
    )
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, help_text="Ex: Carro, Moto, Caminhão")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    
    # Permitir null e blank resolve o IntegrityError (1048)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, null=True, blank=True)
    
    # Alterado para 'motorista' para alinhar com o forms.py e views.py
    motorista = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'perfil': 'entregador'},
        related_name='veiculos'
    )

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

# 4. Cadastro de Clientes
class Cliente(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome Completo")
    documento = models.CharField(max_length=20, unique=True, verbose_name="CPF/CNPJ")
    telefone = models.CharField(max_length=20, verbose_name="WhatsApp/Telefone")
    
    # ENDEREÇO SEPARADO
    rua = models.CharField(max_length=200, verbose_name="Logradouro/Rua")
    numero = models.CharField(max_length=10, verbose_name="Número")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, default="Sua Cidade", verbose_name="Cidade")
    
    # AUXÍLIO AO ENTREGADOR
    ponto_referencia = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Ponto de Referência",
        help_text="Ex: Próximo ao mercado X, portão azul, etc."
    )
    
    observacoes_fixas = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Observações de Entrega",
        help_text="Instruções permanentes para este cliente."
    )

    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    filial = models.ForeignKey('Filial', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Filial Padrão")

    def __str__(self):
        return f"{self.nome} - {self.bairro}"

    # Função útil para mostrar o endereço completo formatado
    @property
    def endereco_completo(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}"

# 5. Registro de Entregas (O coração do sistema)
class Entrega(models.Model):
    STATUS_ENTREGA = (
        ('pendente', 'Pendente'),
        ('em_rota', 'Em Rota'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    filial_origem = models.ForeignKey(Filial, on_delete=models.CASCADE)
    operador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='entregas_criadas')
    entregador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='minhas_entregas')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, blank=True)
    
    # --- CAMPOS QUE FALTAVAM PARA O SEU FORMULÁRIO FUNCIONAR ---
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rua = models.CharField(max_length=200, verbose_name="Rua da Entrega")
    numero = models.CharField(max_length=10, verbose_name="Número")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    ponto_referencia = models.CharField(max_length=255, blank=True, null=True)
    # No seu form você usou 'observacoes', aqui no model está 'observacao_entrega'. 
    # Sugiro manter um nome só para facilitar.
    observacao_entrega = models.TextField(blank=True, null=True) 
    # ----------------------------------------------------------

    status = models.CharField(max_length=20, choices=STATUS_ENTREGA, default='pendente')
    prioridade = models.BooleanField(default=False)
    eh_perecivel = models.BooleanField(default=False, verbose_name="Contém Perecíveis?")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    
    km_saida = models.IntegerField(null=True, blank=True)
    km_chegada = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Entrega #{self.id} - {self.cliente.nome}"