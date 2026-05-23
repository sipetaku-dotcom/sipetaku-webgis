from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-demo-sipetaku'
)

DEBUG = config(
    'DEBUG',
    default=False,
    cast=bool
)

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '187.77.118.171',
    'sipetaku.com',
    'www.sipetaku.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://sipetaku.com',
    'https://www.sipetaku.com',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sekolah',
    'peta',
    'guru',
    'murid',
    'akun',
    'aset',
    'prestasi',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'akun.context_processors.info_operator',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config(
            'DB_NAME',
            default='sipetaku_db'
        ),
        'USER': config(
            'DB_USER',
            default='sipetaku_user'
        ),
        'PASSWORD': config(
            'DB_PASSWORD',
            default='SipetakuDB@2026'
        ),
        'HOST': config(
            'DB_HOST',
            default='localhost'
        ),
        'PORT': config(
            'DB_PORT',
            default='5432'
        ),
    }
}


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


LANGUAGE_CODE = 'id'

TIME_ZONE = 'Asia/Makassar'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'


TURNSTILE_SITE_KEY = config(
    '0x4AAAAAADU2nZWaKW5IiiT5',
    default=''
)

TURNSTILE_SECRET_KEY = config(
    '0x4AAAAAADU2nSZyzCpPutWdBx75zNCbtog',
    default=''
)


SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'