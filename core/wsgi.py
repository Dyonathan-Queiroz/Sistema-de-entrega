import os

from django.core.wsgi import get_wsgi_application

# Define o arquivo de configurações que o servidor deve ler
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Esta é a variável que o Django estava procurando e não achou
application = get_wsgi_application()