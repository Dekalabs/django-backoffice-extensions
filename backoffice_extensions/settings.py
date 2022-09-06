from typing import Any

from django.conf import settings

# Needed to build and publish
# ------------------------------------------------------------------------------
SECRET_KEY = "backoffice"

# Specific project configuration
# ------------------------------------------------------------------------------
def get_backoffice_settings_attribute(attribute: str, default: Any) -> Any:
    """Gets the value from the dict, depending on the BACKOFFICE_SITE value."""
    site = getattr(settings, "BACKOFFICE_SITE", "default")
    return getattr(settings, "BACKOFFICE", {}).get(site, {}).get(attribute, default)


TITLE = get_backoffice_settings_attribute("TITLE", "backoffice")
LOGO = get_backoffice_settings_attribute("LOGO", None)
NONE_VALUE = get_backoffice_settings_attribute("NONE_VALUE", "-")
NO_IMAGE_VALUE = get_backoffice_settings_attribute("NO_IMAGE_VALUE", NONE_VALUE)
URL_NAMESPACE = get_backoffice_settings_attribute("URL_NAMESPACE", "backoffice")
STATUS_FIELDS = get_backoffice_settings_attribute("STATUS_FIELDS", ("status",))
STATUS_TAG_CLASSES = get_backoffice_settings_attribute("STATUS_TAG_CLASSES", {})
DETAILS_URLS = get_backoffice_settings_attribute(
    "DETAILS_URLS",
    [
        {"names": ("pk", "id"), "follow": False},
        {"names": ("user", "owner")},
    ],
)
SIDEBAR_CONFIG = get_backoffice_settings_attribute("SIDEBAR_CONFIG", [])
PRIMARY_COLOR = get_backoffice_settings_attribute("PRIMARY_COLOR", "#011b67")
ACCENT_COLOR = get_backoffice_settings_attribute("ACCENT_COLOR", "#fff")
