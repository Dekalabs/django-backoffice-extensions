from django.urls import path, include

from tests.backoffice.views import IndexView

app_name = "backoffice"
urlpatterns = [
    path("stuffs/", include("tests.backoffice.stuffs.urls")),
    path("users/", include("tests.backoffice.users.urls")),
    path("auth/", include("tests.backoffice.auth.urls")),
    path("", IndexView.as_view(), name="index"),
]
