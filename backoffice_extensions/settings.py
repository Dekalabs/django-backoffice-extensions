from django.conf import settings

# Needed to build and publish
# ------------------------------------------------------------------------------
SECRET_KEY = "backoffice"

# Specific project configuration
# ------------------------------------------------------------------------------
TITLE = getattr(settings, "BACKOFFICE_TITLE", "backoffice")
NONE_VALUE = getattr(settings, "BACKOFFICE_NONE_VALUE", "-")
NO_IMAGE_VALUE = getattr(settings, "BACKOFFICE_NONE_VALUE", NONE_VALUE)
URL_NAMESPACE = getattr(settings, "BACKOFFICE_URL_NAMESPACE", "backoffice")
BOOLEAN_TRUE_ICON_CLASSES = getattr(
    settings,
    "BACKOFFICE_BOOLEAN_TRUE_ICON_CLASSES",
    "has-text-success fas fa-check-circle",
)
BOOLEAN_FALSE_ICON_CLASSES = getattr(
    settings,
    "BACKOFFICE_BOOLEAN_FALSE_ICON_CLASSES",
    "has-text-danger fas fa-times-circle",
)

STATUS_FIELDS = getattr(settings, "BACKOFFICE_STATUS_FIELDS", ("status",))
STATUS_TAG_CLASSES = getattr(settings, "BACKOFFICE_STATUS_TAG_CLASSES", {})
DETAILS_URLS = getattr(
    settings,
    "BACKOFFICE_DETAILS_URLS",
    [
        {"names": ("pk", "id"), "follow": False},
        {"names": ("user", "owner")},
    ],
)
SIDEBAR_CONFIG = getattr(settings, "BACKOFFICE_SIDEBAR_CONFIG", [])

PRIMARY_BG_COLOR = getattr(settings, "BACKOFFICE_PRIMARY_BG_COLOR", "#191988")
PRIMARY_COLOR = getattr(settings, "BACKOFFICE_PRIMARY_COLOR", "#fff")
