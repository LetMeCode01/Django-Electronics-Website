from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-7%-y!9g&owy3mb8kwp2rl-#d_cp$ro033657^n^_fyhi%v%a!#'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'electronice'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proiect_electronice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Lab 4, Task QuerySets, Ex 4 - Context processor pentru categorii
                'electronice.views.get_categorii',
            ],
        },
    },
]

WSGI_APPLICATION = 'proiect_electronice.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Lab 7, Task 1 - Configurare email (development - afiseaza in consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@electronice.com'

# Lab 7, Task 3 - Configurare pentru mail_admins()
# Lista administratorilor care primesc alerte de securitate
ADMINS = [
    ('Admin1', 'mihaisima22@gmail.com'),
    ('Admin2', 'mihaisec22@gmail.com'),
]

# Lab 7, Task 3 - Adresa de email de la care se trimit mesajele catre admini
SERVER_EMAIL = 'server@electronice.com'

# Lab 7, Task 3 - Prefixul pentru subiectul email-urilor catre admini
EMAIL_SUBJECT_PREFIX = '[Electronice Alert] '

# Lab 8, Task 1d - Numarul maxim de accesari 403 permise in sesiune
N_MAX_403 = 5

# Lab 7, Task 4 - Configurare sistem de logging
import os
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {#dictionar Python
    'version': 1,
    'disable_existing_loggers': False,
    
    # Lab 7, Task 4 - Formatteri (simplu pentru consola, verbose pentru fisiere)
    'formatters': {
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
        'verbose': {
            'format': '[{asctime}] [{levelname}] [{name}] [{module}:{lineno}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    
    # Lab 7, Task 4 - Handlers pentru consola si fisiere
    'handlers': {
        # Handler consola - WARNING, ERROR, CRITICAL in format simplu
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Handler fisier debug.log - format verbose
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        # Handler fisier info.log - format verbose
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'info.log'),
            'formatter': 'verbose',
        },
        # Handler fisier warning.log - format verbose
        'file_warning': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'warning.log'),
            'formatter': 'verbose',
        },
        # Handler fisier error.log - format verbose
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'error.log'),
            'formatter': 'verbose',
        },
        # Handler fisier critical.log - format verbose
        'file_critical': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'critical.log'),
            'formatter': 'verbose',
        },
    },
    
    # Lab 7, Task 4 - Logger principal django
    'loggers': {
        'django': {
            'handlers': ['console_warning', 'file_debug', 'file_info', 'file_warning', 'file_error', 'file_critical'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
