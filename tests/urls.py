from django.urls import include, path


urlpatterns = [
    path("backoffice/", include("tests.backoffice.urls", namespace="backoffice")),
]
