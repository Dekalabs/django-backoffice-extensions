from typing import Dict, List, Optional, Type

from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import ProtectedError
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
    form_set_classes: dict = {}

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update({"form_sets": self.form_set_classes})
        return context

    def get_redirect_response(self, instance):
        model_class = self.get_model_class()
        return redirect(
            f"{URL_NAMESPACE}:{model_class._meta.model_name}-detail",
            pk=instance.pk,
        )

    def get(self, request, **kwargs):
        form = self.form_class()
        context = {"form": form}
        context.update(self.get_extra_context())
        return render(request, self.template_name, context=context)

    def after_create(self, instance):
        pass

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form_sets = [
            form_set(data=request.POST, files=request.FILES)
            for form_set in self.form_set_classes.values()
        ]
        if form.is_valid():
            instance = form.save()
            for form_set in form_sets:
                form_set.instance = instance
            if all([form_set.is_valid() for form_set in form_sets]):
                for form_set in form_sets:
                    form_set.save()
                self.after_create(instance)
                messages.success(
                    request, self.success_message.format(instance=str(instance))
                )
                return self.get_redirect_response(instance=instance)
        form_sets_dict = {
            key: form_sets[i] for i, key in enumerate(self.form_set_classes.keys())
        }
        context = {
            "form": form,
            "form_sets": form_sets_dict,
            **self.get_extra_context(),
        }
        return render(request, self.template_name, context=context)


class BackOfficeEditView(BackOfficeFormView):
    """Base view for editions."""

    queryset: Optional[models.QuerySet] = None
    success_message = _("{instance} updated")
    form_set_classes: dict = {}

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update({"form_sets": self.form_set_classes})
        return context

    def get_queryset(self) -> Optional[models.QuerySet]:
        """Gets the queryset in order to be able to access to annotated fields."""
        return self.queryset

    def get_redirect_response(self, instance):
        model_class = self.get_model_class()
        return redirect(
            f"{URL_NAMESPACE}:{model_class._meta.model_name}-detail", pk=instance.pk
        )

    def get(self, request, pk, **kwargs):
        model_class = self.get_model_class()
        queryset = self.get_queryset()
        if queryset:
            instance = get_object_or_404(queryset, pk=pk)
        else:
            instance = get_object_or_404(model_class, pk=pk)
        form = self.form_class(instance=instance)
        context = {
            "form": form,
            "instance": instance,
            "form_sets": {
                label: form_set(instance=instance)
                for label, form_set in self.form_set_classes.items()
            },
            **self.get_extra_context(),
        }
        return render(request, self.template_name, context=context)

    def after_edit(self, instance):
        pass

    def post(self, request, pk, **kwargs):
        model_class = self.get_model_class()
        instance = get_object_or_404(model_class, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=instance)
        context = {"form": form, "instance": instance, **self.get_extra_context()}
        form_sets = [
            form_set(data=request.POST, files=request.FILES, instance=form.instance)
            for form_set in self.form_set_classes.values()
        ]
        if form.is_valid() and all([form_set.is_valid() for form_set in form_sets]):
            instance = form.save()
            for form_set in form_sets:
                form_set.save()
            self.after_edit(instance)
            messages.success(
                request, self.success_message.format(instance=str(instance))
            )
            return self.get_redirect_response(instance=instance)
        form_sets_dict = {
            key: form_sets[i] for i, key in enumerate(self.form_set_classes.keys())
        }
        context.update({"form_sets": form_sets_dict})
        return render(request, self.template_name, context=context)


class BackOfficeListView(LoginRequiredMixin, BackOfficeViewMixin, ListView):
    """Base view for lists."""

    queryset: Optional[models.QuerySet] = None
    list_display: List = []
    filterset_class: Optional[Type] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter = None

    def get_queryset(self):
        """Uses the FilterSet class to filter the query."""
        queryset = super().get_queryset()
        if self.filterset_class:
            self.filter = self.filterset_class(
                self.request.GET, queryset=queryset, request=self.request
            )
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
        if queryset:
            return get_object_or_404(queryset, pk=pk)
        return get_object_or_404(self.model_class, pk=pk)

    def get(self, request, pk):
        self.instance = self.get_object(pk=pk)
        context = {"instance": self.instance, "fields": self.fields}
        context.update(self.get_extra_context())
        return render(request, self.template_name, context=context)


class BackOfficeDeleteView(LoginRequiredMixin, BackOfficeViewMixin, View):
    """Base delete view."""

    uses_template = False
    queryset: Optional[models.QuerySet] = None
    model_class: Type[models.Model] = models.Model
    success_message = _("{instance} deleted")
    protected_error_message = _("{instance} can't be deleted")

    def get_queryset(self) -> Optional[models.QuerySet]:
        """Gets the queryset in order to be able to access to annotated fields."""
        return self.queryset

    def get_redirect_response(self):
        return redirect(f"{URL_NAMESPACE}:{self.model_class._meta.model_name}-list")

    def perform_delete(self, instance):
        """Overwrite to handle the deletion. By default, it uses model delete."""
        instance.delete()

    def get_object(self, pk: int) -> models.Model:
        """Gets the object, using the queryset if provided to add annotation fields."""
        queryset = self.get_queryset()
        if queryset:
            return get_object_or_404(queryset, pk=pk)
        return get_object_or_404(self.model_class, pk=pk)

    def get(self, request, pk, **kwargs):
        """Gets the instance and calls to perform delete."""
        instance = self.get_object(pk=pk)
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

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.sign_in_redirect)
        context = self.get_context_data()
        context.update(self.get_extra_context())
        return render(request, self.template_name, context=context)
