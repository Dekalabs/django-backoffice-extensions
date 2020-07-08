"""Django app made to create backoffices to help the administration of a site, like 
the Django Admin site, but for final users.
"""
from django.utils.module_loading import autodiscover_modules

__version__ = "1.0.2"


default_app_config = "backoffice_extensions.apps.BackofficeAppConfig"
