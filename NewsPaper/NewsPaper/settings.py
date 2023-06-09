"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.
# from dotenv import dotenv_values
# config = dotenv_values(".env")
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^ie1-h=$&v%%-4@$q&0mhm$_hl=gcwnk%u4jd8(khkbyf6)n+e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
# ALLOWED_HOSTS = ['localhost']


# авторизация с allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',

    'django_filters' ,
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',

    'news.apps.NewsConfig',
]

SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'NewsPaper.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # до allauth
        # 'DIRS': [],
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

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

ACCOUNT_FORMS = {'signup': 'news.forms.CommonSignupForm'}

LOGIN_REDIRECT_URL = '/news/'

LOGOUT_REDIRECT_URL = '/news/'

LOGIN_URL = '/accounts/login/' # авторизация с allauth

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER =config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = config("EMAIL_USE_SSL")

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
EMAIL_CHARSET = config("EMAIL_CHARSET")

# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL=LOGIN_URL # кажется не нужно
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL=None
ACCOUNT_EMAIL_SUBJECT_PREFIX='NewsPaper '
ACCOUNT_SIGNUP_REDIRECT_URL=LOGIN_REDIRECT_URL

# if DEBUG:
#     EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

# формат даты, которую будет воспринимать наш задачник(вспоминаем урок по фильтрам) 
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
 
# если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше, но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}


# для отправки почты в файл
EMAIL_FILE_PATH = 'email-messages'
ADMINS = (
    ('admin', 'admin@example.com'),
)

# DEBUG = False
# if DEBUG:
#     # EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
#     EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
        'with_path': {
            # 'format': '%(asctime)s %(levelname)s %(pathname)s %(message)s'
            'format': '%(pathname)s'
        },
        'with_path_stack': {
            # 'format': '%(asctime)s %(levelname)s %(pathname)s %(exc_info)s %(message)s'
            'format': '%(exc_info)s'
        },
        'file_general': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'file_errors': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'
        },
        'to_mail': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_DEBUG': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console_WARNING': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'with_path'
        },
        'console_ERROR': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'with_path_stack'
        },
        'file_INFO': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename' : os.path.join(BASE_DIR, 'logs','general.log'),
            'formatter': 'file_general'
        },
        'file_ERROR': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename' : os.path.join(BASE_DIR, 'logs','errors.log'),
            'formatter': 'file_errors'
        },
        'file_security': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename' : os.path.join(BASE_DIR, 'logs','security.log'),
            'formatter': 'file_general' # формат как в file_INFO
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'to_mail',
            'include_html': True,
            'email_backend': 'django.core.mail.backends.filebased.EmailBackend', # отправлять в файл
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_DEBUG', 'console_WARNING', 'console_ERROR', 'file_INFO'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_ERROR', 'mail_admins'],
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file_ERROR', 'mail_admins'],
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file_ERROR'],
            'propagate': True,
        },
        'django.db_backends': {
            'handlers': ['file_ERROR'],
            'propagate': True,
        },
        'django.security': {
            'handlers': ['file_security'],
            'propagate': True,
        },
    }
}
