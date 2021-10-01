import collections
import csv
import datetime
import io
from typing import Any, Dict, Optional

from django.utils import timezone


def create_csv_from_data(
    data: Dict, stream: Optional["io.StringIO"] = None
) -> "io.StringIO":
    """Creates a CSV stream using the given dict, in where the keys are
    the columns and each value is a list of results.
    """
    stream = io.StringIO() if not stream else stream
    header = list(data.keys())
    writer = csv.DictWriter(stream, fieldnames=data.keys())
    writer.writeheader()
    for index in range(len(data[header[0]])):
        row = {key: data[key][index] for key in header}
        writer.writerow(row)
    return stream


def age_range_filter(
    field: Any, min_age: Optional[int] = None, max_age: Optional[int] = None
) -> Dict:
    """Returns the filter for the age range."""
    current = timezone.now().date()
    _filter = {}
    if min_age:
        _filter[f"{field}__year__lte"] = datetime.date(
            current.year - min_age, current.month, current.day
        ).year
    if max_age:
        _filter[f"{field}__year__gte"] = datetime.date(
            current.year - max_age, current.month, current.day
        ).year
    return _filter


StatisticsValue = collections.namedtuple(
    "StatisticsValue", ["value", "percentage", "help_text"]
)
StatisticsValue.__new__.__defaults__ = (False, None)  # type: ignore
