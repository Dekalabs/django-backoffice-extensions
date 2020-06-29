import os
import sys

from django.core.wsgi import get_wsgi_application

app_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.production")
application = get_wsgi_application()
