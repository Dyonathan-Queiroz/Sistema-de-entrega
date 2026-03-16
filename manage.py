import os
from dotenv import load_dotenv

load_dotenv()

# ... (outras configurações)

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

# 1. Adicione sua app na lista
INSTALLED_APPS = [
    # ... apps padrão do django
    'entregas',
]

# 2. Configure o Banco de Dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# 3. Configure os arquivos estáticos (AdminLTE)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]