from django import forms
from .models import Veiculo, Usuario

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