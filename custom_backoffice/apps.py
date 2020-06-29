from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BackofficeAppConfig(AppConfig):

    name = "custom_backoffice"
    verbose_name = _("Backoffice")
