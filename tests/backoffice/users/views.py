from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from backoffice_extensions.mixins import ExportMixin, SearchListMixin
from backoffice_extensions.views import (
    BackOfficeCreateView,
    BackOfficeDetailView,
    BackOfficeEditView,
    BackOfficeListView,
)
from tests.backoffice.users.forms import CreationUserForm, UserForm

User = get_user_model()


class UserListView(SearchListMixin, BackOfficeListView):
    template_name = "backoffice/users/list.html"
    queryset = User.objects.all().order_by("-date_joined")
    context_object_name = "users"
    search_fields = [
        "first_name",
        "last_name",
        "username",
    ]
    paginate_by = 15
    list_display = ["id", "first_name", "last_name", "username", "date_joined"]


class UserCreateView(BackOfficeCreateView):
    template_name = "backoffice/users/create.html"
    form_class = CreationUserForm


class UserEditView(BackOfficeEditView):
    template_name = "backoffice/users/edit.html"
    form_class = UserForm


class UserDetailView(BackOfficeDetailView):
    template_name = "backoffice/users/detail.html"
    queryset = UserListView.queryset
    model_class = User
    context_object_name = "user"
    fields = [
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
    ]


class ExportUsersView(LoginRequiredMixin, ExportMixin, View):
    filename = "users.csv"
    queryset = UserListView.queryset
    fields = UserDetailView.fields
    filterset_class = UserListView.filterset_class
