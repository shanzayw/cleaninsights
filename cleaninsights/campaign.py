from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Optional

from cleaninsights.aggregation_period import AggregationPeriod
from cleaninsights.aggregation_rule import EventAggregationRule


@dataclass
class Campaign:
    """
    A logical grouping for event and visit measurements.
    This grouping is user-defined and can be bounded by time and with specific
    measurement properties.
    """
    start: date
    """
    The start date for this campaign. Measurements to be recorded before this
    date will be ignored.
    """
    end: date
    """
    The end date for this campaign. Measurements to be recorded before this
    date will be ignored.
    """
    aggregation_period_length: timedelta
    """
    The length of each aggregation period. In "real-time" mode, aggregated data
    will be sent to the analytics server at the end of each aggregation period.
    """
    number_of_periods: Optional[int]
    """
    The number of periods for which to collect measurements from each user. If
    `None` there will be no restriction and measurements will continue until
    the :attr:`end <Campaign.end>`.
    """
    only_record_once: bool
    """
    The event should only be recorded once, it either happened zero times or
    more than zero times within a single aggregation period.
    """
    event_aggregation_rule: EventAggregationRule
    """
    The aggregation rule to be used when recording measurements.
    """
    @property
    def current_measurement_period(
            self) -> Optional[AggregationPeriod]:  # noqa: D401
        """
        Alias for :attr:`Campaign.current_aggregation_period`.
        **Deprecated.** This name is used in the TypeScript and iOS SDKs,
        however is not consistent with usage in the Campaign object.
        """
        return self.current_aggregation_period

    @property
    def current_aggregation_period(
            self) -> Optional[AggregationPeriod]:  # noqa: D401
        """
        The current aggregation period for this campaign.
        The period defines start (inclusive) and end (exclusive) dates. If it
        is currently before or after the campaign's :attr:`start
        <Campaign.start>` or :attr:`end <Campaign.end>` dates, `None` will be
        returned.
        """
        return self.aggregation_period(datetime.utcnow())

    def aggregation_period(
            self, dt: datetime) -> Optional[AggregationPeriod]:  # noqa: D401
        """
        The aggregation period for this campaign in which `dt` falls.
        The period defines start (inclusive) and end (exclusive) dates. If it
        is currently before or after the campaign's :attr:`start
        <Campaign.start>` or :attr:`end <Campaign.end>` dates, `None` will be
        returned.
        """
        d = dt.date()
        if d < self.start or d > self.end:
            return None
        start = self.start
        while True:
            end = start + self.aggregation_period_length
            if end > d:
                break
            start += self.aggregation_period_length
        if end < d:
            return None
        return AggregationPeriod(start, end)

    @classmethod
    def from_dict(cls, campaign_data: Dict[str, Any]):  # -> Campaign
        try:
            aggregation_period_length = timedelta(
                days=campaign_data["aggregation_period_length"])
            number_of_periods = campaign_data["number_of_periods"]
        except KeyError:
            number_of_periods = None
        return Campaign(campaign_data["start"], campaign_data["end"],
                        aggregation_period_length, number_of_periods,
                        campaign_data["only_record_once"],
                        campaign_data["event_aggregation_rule"])
