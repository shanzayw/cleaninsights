from enum import Enum


class EventAggregationRule(Enum):
    """The aggregation rule to use for source aggregation of results."""
    SUM = "sum"
    """Calculate the sum of the values."""
    AVG = "avg"
    """Calculate the mean average of the values."""
