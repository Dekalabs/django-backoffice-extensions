"""Django app made to create backoffices to help the administration of a site, like
the Django Admin site, but for final users.
"""
import django

__version__ = "4.0.0"

if django.VERSION < (3, 2):
    default_app_config = "backoffice_extensions.apps.BackofficeAppConfig"
