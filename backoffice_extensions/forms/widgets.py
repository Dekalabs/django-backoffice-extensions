from django import forms


class Select(forms.Select):
    template_name = "backoffice/widgets/select.html"


class SelectMultiple(forms.SelectMultiple):
    template_name = "backoffice/widgets/select_multiple.html"
