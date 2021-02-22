from datetime import date
from typing import Optional
from typing import Union

from cleaninsights.datapoint import DataPoint


class Event(DataPoint):
    category: str
    action: Optional[str]
    name: Optional[str]
    value: Optional[Union[int, float]]

    def __init__(self, category: str, action: Optional[str],
                 name: Optional[str], value: Optional[Union[int, float]],
                 campaign_id: str, times: Optional[int],
                 first: date, last: date):
        super().__init__(campaign_id, times, first, last)
        self.category = category
        self.action = action
        self.name = name
        self.value = value

    def __repr__(self):
        return (f"<Visit path={self.path} "
                f"action={self.action} "
                f"name={self.name} "
                f"value={self.value} "
                f"campaign_id={self.campaign_id} "
                f"times={self.times} "
                f"first={self.first} "
                f"last={self.last}>")
