"""
WSGI config for tim_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '/var/www/u1763586/data/www/time-money.shop/tim-site')
sys.path.insert(1, '/var/www/u1763586/data/djangoenv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tim_site.settings'

application = get_wsgi_application()
