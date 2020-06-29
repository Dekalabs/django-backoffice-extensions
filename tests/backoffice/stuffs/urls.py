from django.urls import path

from tests.backoffice.stuffs.views import StuffListView, StuffDetailView

urlpatterns = [
    path("<int:pk>/", StuffDetailView.as_view(), name="stuff-detail"),
    path("", StuffListView.as_view(), name="stuff-list"),
]
