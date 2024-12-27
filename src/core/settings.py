from .config import project_config, CacheType
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = project_config.SECRET_KEY

DEBUG = project_config.DEBUG

ALLOWED_HOSTS = project_config.allowed_hosts


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'utils',
    'project',

    # third party
    'django_celery_results',
    'django_celery_beat',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


# Database
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": project_config.DB_NAME,
        "USER": project_config.DB_USER,
        "PASSWORD": project_config.DB_PASSWORD,
        "HOST": project_config.DB_HOST,
        "PORT": project_config.DB_PORT,
        'TEST': {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            'NAME': 'test_db',
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Emails
EMAIL_HOST = project_config.EMAIL_HOST
EMAIL_PORT = project_config.EMAIL_PORT
EMAIL_HOST_USER = project_config.EMAIL_HOST_USER
EMAIL_USE_TLS = project_config.EMAIL_USE_TLS
EMAIL_USE_SSL = project_config.EMAIL_USE_SSL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_PASSWORD = project_config.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# static & media
STATICFILES_DIRS = []

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static_root'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Caches
CACHE_TIMEOUT = project_config.CACHE_TIMEOUT

CACHES = {
    "redis": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "TIMEOUT": CACHE_TIMEOUT,
        "LOCATION": project_config.redis_url,
    },
    "db": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "TIMEOUT": CACHE_TIMEOUT,
        "LOCATION": "django_project_cache",
    },
    "dummy": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "TIMEOUT": CACHE_TIMEOUT,
    }
}
if project_config.CACHE_TYPE in CACHES:
    CACHES["default"] = CACHES[project_config.CACHE_TYPE]
else:
    raise Exception(f"Unsupported {project_config.CACHE_TYPE=}")

# Celery
CELERY_BROKER_URL = project_config.redis_url
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_CACHE_BACKEND = project_config.CELERY_CACHE_BACKEND
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
