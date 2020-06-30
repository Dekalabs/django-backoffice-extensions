from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BackofficeAppConfig(AppConfig):

    name = "backoffice_extensions"
    verbose_name = _("Backoffice")
