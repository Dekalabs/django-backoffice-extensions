from backoffice_extensions.mixins import ExportMixin, SearchListMixin
from backoffice_extensions.views import BackOfficeListView, BackOfficeDetailView
from tests.app.models import Stuff


class StuffListView(BackOfficeListView):
    template_name = "backoffice/stuff/list.html"
    queryset = Stuff.objects.all()
    paginate_by = 15
    list_display = ["id", "status", "owner"]


class StuffDetailView(BackOfficeDetailView):
    template_name = "backoffice/stuff/detail.html"
    queryset = StuffListView.queryset
    model_class = Stuff
    context_object_name = "stuff"
    fields = ["id", "status", "owner"]
