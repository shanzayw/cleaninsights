from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class Campaign:
    start: date
    end: date
    aggregation_period_length: int
    number_of_periods: Optional[int]
    only_record_once: bool
    event_aggregation_rule: str

    @property
    def aggregation_period(self) -> timedelta:
        return timedelta(days=self.aggregation_period_length)

    @property
    def current_measurement_period(self) -> Optional[Dict[str, date]]:
        now = datetime.utcnow().date()
        if now < self.start or now > self.end:
            return None
        start = self.start
        while True:
            end = start + self.aggregation_period
            if end > now:
                break
            start += self.aggregation_period
        if end < now:
            return None
        return {"start": start, "end": end}

    @classmethod
    def from_dict(cls, campaign_data: Dict[str, Any]):  # -> Campaign
        try:
            number_of_periods = campaign_data["number_of_periods"]
        except KeyError:
            number_of_periods = None
        return Campaign(campaign_data["start"], campaign_data["end"],
                        campaign_data["aggregation_period_length"],
                        number_of_periods, campaign_data["only_record_once"],
                        campaign_data["event_aggregation_rule"])
