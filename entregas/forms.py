from django import forms
from .models import Veiculo, Usuario, Filial

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
        def clean_placa(self):
            placa = self.cleaned_data.get('placa')
            return placa.upper() # Salva sempre como ABC-1234

class FilialForm(forms.ModelForm):
    class Meta:
        model = Filial
        fields = ['nome', 'cidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Matriz Centro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: São Paulo'}),
        }

class UsuarioForm(forms.ModelForm):
    # Definimos a senha como um campo de password para não aparecer o texto
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
        user.set_password(self.cleaned_data["password"]) # Criptografa a senha
        if commit:
            user.save()
        return user