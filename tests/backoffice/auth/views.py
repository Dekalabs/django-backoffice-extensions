from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from tests.backoffice.auth.forms import SignInForm


class SignInView(View):
    """View to handle sing-in in the backoffice_extensions."""

    template_name = "backoffice/auth/sign_in.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("backoffice:index")
        context = {"form": SignInForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None:
                login(request, user)
                return redirect("backoffice:index")
        context = {"form": form}
        return render(request, self.template_name, context)


class SignOutView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect("backoffice:index")
