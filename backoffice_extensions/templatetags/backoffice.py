from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db.models import Manager, QuerySet
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.template import defaultfilters
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

from backoffice_extensions.helpers import StatisticsValue
from backoffice_extensions.settings import (
    BOOLEAN_FALSE_ICON_CLASSES,
    BOOLEAN_TRUE_ICON_CLASSES,
    DETAILS_URLS,
    NO_IMAGE_VALUE,
    NONE_VALUE,
    SIDEBAR_CONFIG,
    STATUS_FIELDS,
    STATUS_TAG_CLASSES,
    URL_NAMESPACE,
)

try:
    from django.contrib.gis.geos import Point
except ImproperlyConfigured:
    Point = None


register = template.Library()


@register.inclusion_tag("backoffice/partials/menu.html", takes_context=True)
def sidebar_menu(context):
    """Creates the sidebar data."""
    user = context.get("user")
    request = context.get("request")
    active_path = request.get_full_path_info()
    sidebar = []
    for group in SIDEBAR_CONFIG:
        group_label = group.get("label")
        sections_data = []
        for section, data in group.get("sections").items():
            if data.get("permission") is None or (
                user and user.has_perm(data.get("permission"))
            ):
                url = reverse(f"{URL_NAMESPACE}:{section.lower()}-list")
                active = active_path.startswith(url)
                sections_data.append(
                    (
                        url,
                        data.get("label"),
                        active,
                    )
                )

        # If the group is empty skip it
        if sections_data:
            sidebar.append((group_label, sections_data))

    return {"sidebar": sidebar}


@register.filter
def boolean_icon(value):
    """Gets an icon for given boolean value."""
    result = f'<i class="{BOOLEAN_FALSE_ICON_CLASSES}"></i>'
    if value:
        result = f'<i class="{BOOLEAN_TRUE_ICON_CLASSES}"></i>'
    return mark_safe(result)


@register.filter
def status_tag(value):
    """Gets an icon for given boolean value."""
    result = (
        f'<span class="tag {STATUS_TAG_CLASSES.get(value.status, "")}">'
        f"{value.get_status_display()}</i>"
    )
    return mark_safe(result)


@register.filter(name="getattr")
def getattr_filter(obj, name):
    """Calls to getattr over the given obj with the given name."""

    def _parse_value(value):
        """Parse the given value."""
        if value is None:
            value = NONE_VALUE
        if isinstance(value, bool):
            value = boolean_icon(value)
        if isinstance(value, ImageFieldFile):
            if value:
                value = mark_safe(f'<img src="{value.url}" />')
            else:
                value = NO_IMAGE_VALUE
        if isinstance(value, Manager):
            if value.exists():
                tags = '<div class="tags">'
                for item in value.all():
                    tags += f'<span class="tag">{str(item)}</span>'
                value = mark_safe(tags + "</div>")
            else:
                value = NONE_VALUE
        if Point and isinstance(value, Point):
            value = f"{value.y},{value.x}"
        if isinstance(value, FieldFile) and "csv" in value.name:
            value = mark_safe(
                f'<a href="{value.url}" type="text/csv" download>{value.name}</a>'
            )
        return value

    if isinstance(name, tuple) and len(name) > 0:
        name = name[0]
    result = getattr(obj, name)
    if result is None:
        result = "-"
    for detail_url_data in DETAILS_URLS:
        names = detail_url_data.get("names", tuple())
        follow = detail_url_data.get("follow", True)
        lookup_field = detail_url_data.get("lookup_field") or "pk"
        lookup_field_value = (
            getattr(result, lookup_field) if hasattr(result, lookup_field) else result
        )
        target_model = result if follow else obj
        if name in names:
            try:
                details_url = reverse(
                    f"{URL_NAMESPACE}:{target_model._meta.model_name}-detail",
                    kwargs={lookup_field: lookup_field_value},
                )
                result = mark_safe(f'<a href="{details_url}">{str(result)}</a>')
            except (NoReverseMatch, AttributeError):
                result = result
    if name in STATUS_FIELDS:
        result = status_tag(obj)
    if hasattr(result, "__call__") and not isinstance(result, Manager):
        result = result()
    return _parse_value(result)


@register.filter
def verbose_name(model_or_queryset, field):
    """Gets the verbose name of the given model field."""
    model = model_or_queryset
    if isinstance(field, tuple) and len(field) > 1:
        return field[1]
    if isinstance(model_or_queryset, QuerySet):
        model = model_or_queryset.model
    try:
        return model._meta.get_field(field).verbose_name
    except FieldDoesNotExist:
        if hasattr(model, field) and hasattr(getattr(model, field), "verbose_name"):
            return getattr(getattr(model, field), "verbose_name")
    return field


@register.filter
def statistics_value(value):
    if not isinstance(value, StatisticsValue):
        return intcomma(value)
    result = f"{intcomma(value.value)}"
    if value.percentage:
        result = f"{defaultfilters.floatformat(value.value, 2)} %"
    return result
