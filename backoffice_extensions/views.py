from typing import Dict, List, Optional, Type

from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView

from backoffice_extensions.mixins import BackOfficeViewMixin
from backoffice_extensions.settings import URL_NAMESPACE

User = get_user_model()


class BackOfficeFormView(LoginRequiredMixin, BackOfficeViewMixin, View):
    """Base view for forms."""

    form_class: Type[forms.ModelForm] = forms.ModelForm

    def get_model_class(self) -> Type[models.Model]:
        """Extracts the model class form the ModelFrom."""
        return self.form_class._meta.model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.form_class or not issubclass(self.form_class, forms.ModelForm):
            raise NotImplementedError(
                "You should specify the form_class attribute, and it have to be a "
                "subclass of django.forms.ModelForm"
            )


class BackOfficeCreateView(BackOfficeFormView):
    """Base view for creations."""

    success_message: str = _("{instance} created")

    def get(self, request):
        form = self.form_class()
        context = {"form": form}
        context.update(self.get_extra_context())
        return render(request, self.template_name, context=context)

    def post(self, request):
        model_class = self.get_model_class()
        form = self.form_class(request.POST, request.FILES)
        context = {"form": form}
        context.update(self.get_extra_context())
        if form.is_valid():
            instance = form.save()
            messages.success(
                request, self.success_message.format(instance=str(instance))
            )
            return redirect(
                f"{URL_NAMESPACE}:{model_class._meta.model_name}-detail", pk=instance.pk
            )
        return render(request, self.template_name, context=context)


class BackOfficeEditView(BackOfficeFormView):
    """Base view for editions."""

    success_message = _("{instance} updated")

    def get_redirect_response(self, instance):
        model_class = self.get_model_class()
        return redirect(
            f"{URL_NAMESPACE}:{model_class._meta.model_name}-detail", pk=instance.pk
        )

    def get(self, request, pk):
        model_class = self.get_model_class()
        instance = get_object_or_404(model_class, pk=pk)
        form = self.form_class(instance=instance)
        context = {"form": form, "instance": instance}
        context.update(self.get_extra_context())
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        model_class = self.get_model_class()
        instance = get_object_or_404(model_class, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=instance)
        context = {"form": form, "instance": instance}
        context.update(self.get_extra_context())
        if form.is_valid():
            instance = form.save()
            messages.success(
                request, self.success_message.format(instance=str(instance))
            )
            return self.get_redirect_response(instance=instance)
        return render(request, self.template_name, context=context)


class BackOfficeListView(LoginRequiredMixin, BackOfficeViewMixin, ListView):
    """Base view for lists."""

    list_display: List = []
    filterset_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter = None

    def get_queryset(self):
        """Uses the FilterSet class to filter the query."""
        queryset = super().get_queryset()
        if self.filterset_class:
            self.filter = self.filterset_class(self.request.GET, queryset=queryset)
            queryset = self.filter.qs
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({"list_display": self.list_display, "filter": self.filter})
        context.update(self.get_extra_context())
        return context


class BackOfficeDetailView(LoginRequiredMixin, BackOfficeViewMixin, View):
    """Base detail view."""

    queryset: Optional[models.QuerySet] = None
    model_class: Type[models.Model] = models.Model
    fields: List = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.instance: Optional[models.Model] = None

    def get_queryset(self) -> Optional[models.QuerySet]:
        """Gets the queryset in order to be able to access to annotated fields."""
        return self.queryset

    def get_object(self, pk: int) -> models.Model:
        """Gets the object, using the queryset if provided to add annotation fields."""
        queryset = self.get_queryset()
        if not queryset:
            return get_object_or_404(self.model_class, pk=pk)
        instance = queryset.filter(pk=pk).first()
        if not instance:
            raise Http404
        return instance

    def get(self, request, pk):
        self.instance = self.get_object(pk=pk)
        context = {"instance": self.instance, "fields": self.fields}
        context.update(self.get_extra_context())
        return render(request, self.template_name, context=context)


class BackOfficeDeleteView(LoginRequiredMixin, BackOfficeViewMixin, View):
    """Base delete view."""

    uses_template = False
    model_class: Type[models.Model] = models.Model
    success_message = _("{instance} deleted")
    protected_error_message = _("{instance} can't be deleted")

    def get_redirect_response(self):
        return redirect(f"{URL_NAMESPACE}:{self.model_class._meta.model_name}-list")

    def perform_delete(self, instance):
        """Overwrite to handle the deletion. By default, it uses model delete."""
        instance.delete()

    def get(self, request, pk):
        """Gets the instance and calls to perform delete."""
        instance = get_object_or_404(self.model_class, pk=pk)
        instance_str = str(instance)
        try:
            self.perform_delete(instance=instance)
            messages.success(
                request, self.success_message.format(instance=instance_str)
            )
        except ProtectedError:
            messages.error(
                request, self.protected_error_message.format(instance=instance_str)
            )
        return self.get_redirect_response()


class BackOfficeIndexView(BackOfficeViewMixin, View):
    """Home view of the backoffice_extensions."""

    template_name = "backoffice/index.html"
    sign_in_redirect: str = f"{URL_NAMESPACE}:sign-in"

    @staticmethod
    def default_queryset() -> Dict:
        """Default queryset to each model used in statistics."""
        return {}

    def get_context_data(self) -> Dict:
        """Overwrite to add context to the view."""
        return {}

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(self.sign_in_redirect)
        context = self.get_context_data()
        context.update(self.get_extra_context())
        return render(request, self.template_name, context=context)
