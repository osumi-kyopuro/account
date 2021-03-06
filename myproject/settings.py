"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w_!b139(#q3(=$9pqr5^(3q=hiw52_zji$5o#8_t_mbx%7@a$x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

#CERT_ROOT = os.path.join(BASE_DIR, '.well-known')
#CERT_URL = '/.well-known/'

#CORS_REPLACE_HTTPS_REFERER      = False
#HOST_SCHEME                     = "http://"
#SECURE_PROXY_SSL_HEADER         = None
#SECURE_SSL_REDIRECT             = False
#SESSION_COOKIE_SECURE           = True
#CSRF_COOKIE_SECURE              = True
#SECURE_HSTS_SECONDS             = None
#SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
#SECURE_FRAME_DENY               = False


ALLOWED_HOSTS = ['osumi.pythonanywhere.com','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'attendance2',
    'bootstrap_datepicker_plus',
    #'sslserver'
    #'bootstrap4'
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

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='osumiyuki1123@gmail.com'
EMAIL_HOST_PASSWORD='*19991123Oy'
EMAIL_PORT=587
EMAIL_USE_TLS=True






AUTH_USER_MODEL = 'myapp.CustomUser'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'index'

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'


MEDIA_ROOT=os.path.join(BASE_DIR, 'media')
MEDIA_URL='/image/'

STATIC_URL = '/static/'
STATIC_ROOT  =  "/home/osumi/.virtualenvs/myenv/lib/python3.6/site-packages/bootstrap_datepicker_plus/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
