
from datetime import timedelta
from pathlib import Path
import os



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8s-3p(w9m1oo!6exe@4bod0q67$w)-#^tn#ms-icv7&#5n2i@='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["bazikacho.ir","backend.bazikacho.ir","localhost","dl.bazikacho.ir","127.0.0.1"]




AUTH_USER_MODEL = 'myapp.CustomUser'



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'corsheaders',
    'django_jsonform',
    'ckeditor',
    'rest_framework',
   
    
]
   
    

MIDDLEWARE = [
    # ...
   'myapp.middlewares.TokenMiddleware',
    # ...
]



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.bazikacho.ir'  
EMAIL_PORT = 465  
EMAIL_USE_SSL = True  
EMAIL_HOST_USER = 'support@bazikacho.ir'  
EMAIL_HOST_PASSWORD = '773148javad' 
EMAIL_HOST_USER_CONTACT_US = 'support@bazikacho.ir'  





EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.bazikacho.ir'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER_2 = 'info@bazikacho.ir'
EMAIL_HOST_PASSWORD = '773148javad'
EMAIL_HOST_USER_SEND_NEWSLETTER = 'info@bazikacho.ir'






REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        
    ]
    
}
    
    
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default':
        {
            'toolbar': 'full',
            'width': 'auto',
            'extraPlugins': ','.join([
                'codesnippet',
            ]),
        },
}



CORS_ALLOWED_ORIGINS = [
   
    
    "http://localhost:3000",
    "https://bazikacho.ir",
    "https://dl.bazikacho.ir",
    "https://backend.bazikacho.ir",
    


]


CORS_ORIGIN_ALLOW_ALL = False





MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


]


CORS_ORIGIN_ALLOW_ALL = True


ROOT_URLCONF = 'myapp.urls'

TEMPLATES = [
    
    
    {   'DIRS': [os.path.join(BASE_DIR, 'myapp/templates')],
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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


WSGI_APPLICATION = 'myapp.wsgi.application'





DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '773148',
        'HOST': 'localhost',
        'PORT': '5432'
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


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',  
    }
}






LANGUAGE_CODE = 'fa' 

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


LANGUAGE_CODE = 'en-us'



TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


