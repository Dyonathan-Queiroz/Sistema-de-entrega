from django.contrib import admin
from .models import Filial, Usuario, Veiculo, Cliente, Entrega

# Isso faz com que as tabelas apareçam no painel administrativo
admin.site.register(Filial)
admin.site.register(Usuario)
admin.site.register(Veiculo)
admin.site.register(Cliente)
admin.site.register(Entrega)