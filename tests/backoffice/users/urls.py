from django.urls import path

from tests.backoffice.users.views import (
    ExportUsersView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserEditView,
    UserListView,
)

urlpatterns = [
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("<int:pk>/edit/", UserEditView.as_view(), name="user-edit"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("export/", ExportUsersView.as_view(), name="user-export"),
    path("", UserListView.as_view(), name="user-list"),
]
