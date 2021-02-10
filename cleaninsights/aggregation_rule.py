from enum import Enum


class EventAggregationRule(Enum):
    """Calculate the sum of the values."""
    SUM = "sum"
    """Calculate the mean average of the values."""
    AVG = "avg"
