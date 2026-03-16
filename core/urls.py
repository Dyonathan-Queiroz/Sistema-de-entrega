from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Isso conecta as URLs da sua pasta 'entregas' ao projeto principal
    path('', include('entregas.urls')), 
]