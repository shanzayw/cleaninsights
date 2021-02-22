from datetime import date
from typing import Optional


class DataPoint:
    campaign_id: str
    times: int
    first: date
    last: date

    def __init__(self, campaign_id: str, times: Optional[int],
                 first: date, last: date):
        self.campaign_id = campaign_id
        self.times = 1 if times is None else times
        self.first = first
        self.last = last
