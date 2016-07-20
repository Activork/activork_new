"""
Django settings for activork_new project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

#REST_SESSION_LOGIN = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z^kkm53wo-!5=0khs7v(qpx66-gu4*(m2u0y!8q1@%r!g$=e@t'
GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyAAxeABeKFSGuexhfPIWxDd5bWhg57IUsI'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

AUTH_USER_MODEL = "django_social_app.MyUser"
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_SIGNUP_FORM_CLASS = 'django_social_app.forms.SignupForm'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True



EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "metawing30@gmail.com"
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = "metawing@30"
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


from config import *




NOTIFICATIONS_USE_JSONFIELD=True



PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = []

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'


GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 100,
}

GEOPOSITION_MARKER_OPTIONS = {
    'cursor': 'move'
}



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'myapp',
    'geoposition',
    'notifications',
    'multiselectfield',
    'django_social_app',
    'rest_framework',
    'social.apps.django_app.default',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'easy_thumbnails',
    'image_cropping',
    'article',
    'embed_video',
)


from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates','allauth')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
		'django.contrib.auth.context_processors.auth',
    		'django.core.context_processors.debug',
    		'django.core.context_processors.i18n',
    		'django.core.context_processors.media',
    		'django.core.context_processors.static',
    		'django.core.context_processors.tz',
    		'django.contrib.messages.context_processors.messages',
    		'django.core.context_processors.request',
    		'allauth.account.context_processors.account',
                'django.template.context_processors.request',
                #'django.contrib.auth.context_processors.auth',
                #'django.core.context_processors.debug',
                #'django.core.context_processors.i18n',
                #'django.core.context_processors.media',
                #'django.core.context_processors.static',
                #'django.core.context_processors.tz',
                #'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]



SITE_ID = 1

LOGIN_REDIRECT_URL = '/self_profile/'
SOCIALACCOUNT_QUERY_EMAIL = True

AUTHENTICATION_BACKENDS = (
    'social.backends.linkedin.LinkedinOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


"""TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)"""




ROOT_URLCONF = 'activork_new.urls'

WSGI_APPLICATION = 'activork_new.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
