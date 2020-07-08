from tests.app.constants import ACTIVE, ERROR, IDLE
from django.utils.translation import gettext_lazy as _

DEBUG = True
USE_TZ = True

SECRET_KEY = "dummy"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

INSTALLED_APPS = [
    "django.forms",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "backoffice_extensions",
    "tests.app.apps.TestAppConfig",
    "tests.backoffice.apps.BackofficeAppConfig",
]

ROOT_URLCONF = "tests.urls"
SITE_ID = 1
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English")]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
STATIC_URL = "/static/"
WSGI_APPLICATION = "tests.wsgi.application"

# DJANGO BACKOFFICE
# ------------------------------------------------------------------------------
BACKOFFICE_STATUS_TAG_CLASSES = {
    IDLE: "is-warning",
    ACTIVE: "is-success",
    ERROR: "is-danger",
}
BACKOFFICE_SIDEBAR_CONFIG = [
    {
        "label": _("Data"),
        "sections": {
            "user": {"label": _("User"), "permission": None,},
            "stuff": {"label": _("Stuff"), "permission": None,},
        },
    }
]
