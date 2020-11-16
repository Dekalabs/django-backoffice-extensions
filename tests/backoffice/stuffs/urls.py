from django.urls import path

from tests.backoffice.stuffs.views import (
    StuffDeleteView,
    StuffDetailView,
    StuffListView,
)

urlpatterns = [
    path("<int:pk>/delete/", StuffDeleteView.as_view(), name="stuff-delete"),
    path("<int:pk>/", StuffDetailView.as_view(), name="stuff-detail"),
    path("", StuffListView.as_view(), name="stuff-list"),
]
