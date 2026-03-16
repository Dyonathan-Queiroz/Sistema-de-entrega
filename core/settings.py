import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Definição do BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Carregar variáveis do arquivo .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 3. Configurações de Segurança
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-mude-isso-em-producao')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = []

# 4. Definição das Aplicações (Apps)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Sua App de Entregas
    'entregas',
]

# 5. Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# 6. Configuração de Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# 7. Configuração do Banco de Dados MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# 8. Modelo de Usuário Customizado
AUTH_USER_MODEL = 'entregas.Usuario'

# 9. Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# 10. Arquivos Estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 11. Configuração de campos de ID
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- O QUE ESTAVA FALTANDO ---
# 12. Configurações de Redirecionamento de Login
# Isso impede o erro 404 ao tentar acessar /accounts/login/
LOGIN_URL = 'login'              # Nome da URL na sua entregas/urls.py
LOGIN_REDIRECT_URL = 'dashboard' # Para onde vai após logar com sucesso
LOGOUT_REDIRECT_URL = 'login'    # Para onde vai após clicar em sair