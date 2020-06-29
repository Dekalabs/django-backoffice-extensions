from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class SignInForm(forms.Form):
    """Form to access to the platform."""

    error_css_class = "is-danger"
    username = forms.fields.CharField(
        label=_("Username"),
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": _("Username"),
                "autocapitalize": "off",
                "autocorrect": "off",
                "autofocus": "autofocus",
            }
        ),
        error_messages={"required": _("The username is mandatory")},
    )
    password = forms.fields.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": _("Password")}
        ),
        error_messages={"required": _("The password is mandatory")},
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("These credentials are not correct"))
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError(_("These credentials are not correct"))
        except User.DoesNotExist:
            pass
        return password
