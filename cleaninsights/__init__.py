from datetime import datetime
from typing import Callable
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from cleaninsights.campaign import Campaign
from cleaninsights.conf import Configuration
from cleaninsights.datapoint import DataPoint
from cleaninsights.event import Event
from cleaninsights.store import Store
from cleaninsights.visit import Visit

D = TypeVar('D', DataPoint, Event, Visit)


class CleanInsights:
    conf: Configuration
    store: Store
    persistence_counter: int

    def __init__(self, conf, store):
        self.conf = conf
        self.store = store

    def measure_visit(self, path: List[str], campaign_id: str) -> None:
        campaign = self.get_campaign_if_good(campaign_id, campaign_id)
        if campaign is None:
            self.persist_and_send()
            return
        where: Callable[[Visit],
                        bool] = lambda v: "/".join(v.path) == "/".join(path)
        visit = self.get_and_measure(self.store.visits, campaign_id, campaign,
                                     where)
        if visit is None:
            period = campaign.current_measurement_period
            if period is None:
                return
            visit = Visit(path, campaign_id, None, period.start, period.end)
            self.store.visits.append(visit)

    def measure_event(self,
                      category: str,
                      action: str,
                      campaign_id: str,
                      name: Optional[str] = None,
                      value: Union[int, float] = None):
        raise NotImplementedError

    @property
    def feature_consents(self) -> List[str]:
        raise NotImplementedError

    @property
    def campaign_consents(self) -> List[str]:
        raise NotImplementedError

    def feature_consent_by_index(self, index: int):
        raise NotImplementedError

    def campaign_consent_by_index(self, index: int):
        raise NotImplementedError

    def grant_feature(self, feature):
        raise NotImplementedError

    def deny_feature(self, feature):
        raise NotImplementedError

    def grant_campaign(self, campaign_id: str):
        raise NotImplementedError

    def deny_campaign(self, campaign_id: str):
        raise NotImplementedError

    def is_campaign_currently_granted(self, campaign_id: str) -> bool:
        raise NotImplementedError

    def persist(self) -> None:
        raise NotImplementedError

    def persist_and_send(self) -> None:
        raise NotImplementedError

    def get_campaign_if_good(self, campaign_id: str,
                             debug_str: str) -> Optional[Campaign]:
        campaign = self.conf.campaigns.get(campaign_id, None)
        if campaign is None:
            return None
        now = datetime.utcnow().date()
        if now < campaign.start or now > campaign.end:
            print(f"Measurement {debug_str} discarded, because campaign "
                  f"{campaign_id}' didn't start yet or already finished.")
            return None
        # TODO: Check for consent granted
        return campaign

    def get_and_measure(self, haystack: List[D], campaign_id: str,
                        campaign: Campaign,
                        where: Callable[[D], bool]) -> Optional[D]:
        period = campaign.current_measurement_period
        if period is None:
            return None

        def is_needle(d: D):
            return (period is not None and d.campaign_id == campaign_id
                    and d.first >= period.start and d.first <= period.end
                    and d.last >= period.start and d.last <= period.end
                    and where(d))

        datapoint = next(iter([d for d in haystack if is_needle(d)]), None)
        if datapoint is None:
            return None
        if not campaign.only_record_once:
            datapoint.times += 1
        return datapoint
