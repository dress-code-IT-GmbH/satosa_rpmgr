from satosa_rpmgr.settings_base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<generate a new value, e.g. with openssl rand -base64 30>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

MIDDLEWARE.remove('django.middleware.csrf.CsrfViewMiddleware')  # Proxy deployment - restrict app to Intranet

