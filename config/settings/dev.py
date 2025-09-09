from .base import *
from decouple import config, Csv
from corsheaders.defaults import default_headers

DEBUG = True

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# CORS
CORS_ALLOWED_ORIGINS = [o.strip() for o in config("CORS_ALLOWED_ORIGINS", cast=Csv())]
CORS_ALLOW_HEADERS = list(default_headers) + [
    "authorization",
]
CORS_ALLOW_CREDENTIALS = False  # si JWT va en headers, no cookies
