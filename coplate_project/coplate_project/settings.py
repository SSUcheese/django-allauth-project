"""
Django settings for coplate_project project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os, json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
secret_file = os.path.join(BASE_DIR, 'secrets.json') # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'coplate', # template 오버라이딩 시도하려면 이거 적어두는 순서 유의하자. django는 위에서부터 아래로 내려가면서 찾는다
    'widget_tweaks',
    'django.contrib.sites', # 비슷한 기능 갖는 사이트들 django project 하나로 돌릴 수 있게 해준다.
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

SITE_ID = 1 # 저기 여러 사이트 돌리는 installed app에서 이 사이트 번호가 들어가야 한다.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coplate_project.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'coplate_project.wsgi.application'


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
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # }, 위에가 기본적으로 제공하는 validator 아래는 우리가 넣을 커스텀한 validator
    {
        "NAME" : "coplate.validators.CustomPasswordValidator",
    }
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "ko" #'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Auth Settings

AUTH_USER_MODEL = "coplate.User" # 유저 모델을 사용하겠다는 알림의 의미임. 꼭 써주자

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_SIGNUP_REDIRECT_URL = "index" # 로그인 회원가입 url 자동으로 설정되던 부분 수정
LOGIN_REDIRECT_URL = "index"
ACCOUNT_LOGOUT_ON_GET = True # 이 상태로 두면 false와는 달리 바로 로그아웃이 된다.
ACCOUNT_AUTHENTICATION_METHOD = "email" # 원래는 username이 디폴트, 둘 다 쓰려면 "username_email" 이렇게 적어줘야 한다.
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_FORM_CLASS = "coplate.forms.SignupForm" # signup시에 저거 폼 쓰자는 의미
ACCOUNT_SESSION_REMEMBER = True # 기본값은 false로 되어있음
SESSION_COOKIE_AGE = 3600 # 기본값은 2주 python manage.py clearsessions
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True # 입력한 폼에 오류가 있어도 이거 true로 해두면 비번 날리지 않고 남겨준다.
ACCOUNT_EMAIL_VARIFICATION = "optioanl" # mendatory는 이메일 인증을 완료하기 전까지 로그인 불가  //  optional 회원가입시에 인증메일은 발송, 인증 안 해도 로그인 가능  //  none  인증메일도 없고 필요도 없음 // 참고로 기본값은 optional
ACCOUNT_CONFIRM_EMAIL_ON_GET = True # https://stackoverflow.com/questions/28248647/django-allauth-account-confirm-email-on-get-confusion
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "account_email_confirmation_done" # 유저가 로그인이 됐을 때 이메일 인증 후 넘어가는 페이지
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "account_email_confirmation_done" # 유저가 로그인이 안 됐을 때 이메일 인증 후 넘어가는 페이지
PASSWORD_RESET_TIMEOUT_DAYS = 3
ACCOUNT_EMAIL_SUBJECT_PREFIX ="" # account 이메알 제목의 앞에 붙는 문자열을 빈 문자열로 만든다. 왜냐면 allauth가 발송하는 이메일의 가장 앞에는 오버라이딩 해도 항상 웹사이트 도메인이 앞에 붙음. 그거 없애기 위해서 하는거임 


# Email settings

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# 터미널 콘솔로 이메일 보내는 그런 기능 // 나중에 보완한다. 이거는 우리가 임의로 커스텀한 내용
# https://django-allauth.readthedocs.io/en/latest/installation.html 이거 참고하자
