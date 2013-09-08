import os
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Petar Radosevic', 'petar@wunki.org'),
    ('Martijn van der Veen', 'turiphro@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'pimpin.db',
    }
}

ALLOWED_HOSTS = ['*']
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../public/media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, '../public/static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'i!l0s2b17c6y96kg@de8*kdgita2e7s)-z!bdn&5@bu$^bsirw'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'pimpin.urls'
WSGI_APPLICATION = 'pimpin.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, '../templates'),
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'south',
    'tastypie',
    'social_auth',
    
    'connection',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# API keys for scores
API_KLOUT_KEY       = "dgde2ds2h5csr7jnvnkappyg"
API_KLOUT_SECRET    = "qr68YUbXBM"
API_LINKEDIN_KEY    = "qjcbymj6d313"
API_LINKEDIN_SECRET = "zGdC45PkN29wa91X"
API_TWITTER_KEY     = "2omOsYngfIrCyJMW6H2cw"
API_TWITTER_SECRET  = "z1pXCdqzM1rsWoMTSdpjfIK6cUT14cWx7NQB2FxqE"
API_TWITTER_TOKEN_KEY    = "472339266-ERznGJPxwwz0FZHXWrI3Rs7jL2gi73Ftygub2s8s"
API_TWITTER_TOKEN_SECRET = "gMy6pihh4HrnpPlMoCp0HVess8vGeWt0fudVnevx44"


# Tastypie settings
TASTYPIE_DEFAULT_FORMATS = ['json',]

# Social login
TWITTER_CONSUMER_KEY = 'JrWzRSTEwd47AR0QvJCmw'
TWITTER_CONSUMER_SECRET = 'bVDtYS0dAaoM0z52jA0HU8upWXQjDl4fqJx0yiLnT4'
LOGIN_REDIRECT_URL = '/'
