"""
WSGI config for Tcc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/ubuntu/Tcc')
os.environ.setdefault("PYTHON_EGG_CACHE", "/home/ubuntu/Tcc/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Tcc.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
