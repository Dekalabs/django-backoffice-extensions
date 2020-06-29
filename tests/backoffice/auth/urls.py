from django.urls import path

from tests.backoffice.auth.views import SignInView, SignOutView

urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("sign-out/", SignOutView.as_view(), name="sign-out"),
]
