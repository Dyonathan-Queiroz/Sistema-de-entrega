from django import forms
from .models import Veiculo, Usuario, Filial, Cliente, Entrega

class VeiculoForm(forms.ModelForm):
    TIPO_CHOICES = (
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('caminhao', 'Caminhão'),
    )

    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    motorista = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(perfil='entregador'),
        required=False,
        label="Motorista Responsável",
        empty_label="Nenhum (Disponível)",
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'tipo', 'status', 'motorista']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABC-1234'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Fiat Fiorino'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    # Corrigida a indentação (estava dentro do Meta antes)
    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        return placa.upper() if placa else placa

class FilialForm(forms.ModelForm):
    class Meta:
        model = Filial
        fields = ['nome', 'cidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Matriz Centro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Boa Vista'}),
        }

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'perfil', 'filial', 'veiculo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'perfil': forms.Select(attrs={'class': 'form-control'}),
            'filial': forms.Select(attrs={'class': 'form-control'}),
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'documento', 'telefone', 'rua', 'numero', 'bairro', 'cidade', 'ponto_referencia', 'observacoes_fixas']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'ponto_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes_fixas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class LancarEntregaForm(forms.ModelForm):

    valor = forms.DecimalField(required=False, initial=0)
    # Campo extra que não está no model de Cliente, mas está na Entrega
    eh_pereciveis = forms.BooleanField(
        required=False, 
        label="Possui Perecíveis?",
        widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'customSwitch1'})
    )

    class Meta:
        model = Entrega  # <--- MUDAR DE 'Cliente' PARA 'Entrega'
        fields = [
            'valor', 'entregador', 'veiculo', 'rua', 
            'numero', 'bairro', 'ponto_referencia', 
            'observacao_entrega', 'eh_pereciveis'
        ]
        widgets = {
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'ponto_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'observacao_entrega': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }