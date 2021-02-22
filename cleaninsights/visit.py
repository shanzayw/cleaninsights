from datetime import date
from typing import List
from typing import Optional

from cleaninsights.datapoint import DataPoint


class Visit(DataPoint):
    path: List[str]

    def __init__(self, path: List[str], campaign_id: str, times: Optional[int],
                 first: date, last: date):
        super().__init__(campaign_id, times, first, last)
        self.path = path

    def __repr__(self):
        return (f"<Visit path={self.path} "
                f"campaign_id={self.campaign_id} "
                f"times={self.times} "
                f"first={self.first} "
                f"last={self.last}>")
