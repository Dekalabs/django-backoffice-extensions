import django_filters
from django.utils.translation import gettext_lazy as _
from django_filters.widgets import DateRangeWidget

from django.contrib.auth.models import User


class UserFilter(django_filters.FilterSet):
    date_joined = django_filters.DateFromToRangeFilter(
        widget=DateRangeWidget(attrs={"class": "input", "type": "date"})
    )

    class Meta:
        model = User
        fields = ["date_joined"]
