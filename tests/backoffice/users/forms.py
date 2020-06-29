from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "username": forms.EmailInput(attrs={"class": "input"}),
        }


class CreationUserForm(UserForm):
    class Meta(UserForm.Meta):
        fields = ["password"] + UserForm.Meta.fields
        widgets = dict(
            list(UserForm.Meta.widgets.items())
            + list({"password": forms.PasswordInput(attrs={"class": "input"})}.items())
        )
