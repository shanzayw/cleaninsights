from datetime import date
from typing import NamedTuple


class AggregationPeriod(NamedTuple):
    """An aggregation period with a defined start and end date."""
    start: date
    """The start date."""
    end: date
    """The end date."""
