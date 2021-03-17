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
    """Core class for the CleanInsights SDK."""
    conf: Configuration
    store: Store
    persistence_counter: int
    failed_submission_dt: datetime
    failed_submission_count: int


    def __init__(self, conf, store):
        self.conf = conf
        self.store = store
        self.persistence_counter = 0
        self.failed_submission_count = 0

    def measure_visit(self,
                      path: List[str],
                      campaign_id: str,
                      dt: Optional[datetime] = None) -> None:
        """Measure a visit."""
        if dt is None:
            dt = datetime.utcnow()
        campaign = self.get_campaign_if_good(campaign_id, campaign_id, dt)
        if campaign is None:
            self.persist_and_send()
            return
        where: Callable[[Visit],
                        bool] = lambda v: "/".join(v.path) == "/".join(path)
        visit = self.get_and_measure(self.store.visits, campaign_id, campaign,
                                     where, dt)
        if visit is None:
            period = campaign.aggregation_period(dt)
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
        """Measure an event."""
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
        this.persist()
        if failed_submission_count > 0:
            now = self.datetime.datetime.utcnow()
            exp_retry_allowed_at = self.failed_submission_dt + (self.conf.timeout * (2 ** self.failed_submission_count))
            trn_retry_allowed_at = self.failed_submission_dt + timedelta(minutes=self.conf.max_retry_delay)
            if trn_retry_allowed_at < exp_retry_allowed_at:
                retry_allowed_at = trn_retry_allowed_at
                failed_submission_dt = now
            else:
                retry_allowed_at = exp_retry_allowed_at
            if now < retry_allowed_at:
                return
        insights = self.store._generate_insights()
        if self.store.send(insights, self.conf.server, self.conf.timeout):
            pass  # TODO: Remove submitted results from the store
            self.failed_submission_count = 0
        else:
            pass  # TODO: Increase backoff timer https://gitlab.com/cleaninsights/clean-insights-js-sdk/-/issues/5
            if self.failed_submission_count == 0:
                self.failed_submission_dt = datetime.datetime.utcnow()
            self.failed_submission_count += 1

    def get_campaign_if_good(
            self,
            campaign_id: str,
            debug_str: str,
            dt: Optional[datetime] = None) -> Optional[Campaign]:
        campaign = self.conf.campaigns.get(campaign_id, None)
        if campaign is None:
            return None
        now = dt.date() if dt is not None else datetime.utcnow().date()
        if now < campaign.start or now > campaign.end:
            print(f"Measurement {debug_str} discarded, because campaign "
                  f"{campaign_id}' didn't start yet or already finished.")
            return None
        # TODO: Check for consent granted
        return campaign

    def get_and_measure(self, haystack: List[D], campaign_id: str,
                        campaign: Campaign,
                        where: Callable[[D], bool],
                        dt: Optional[datetime] = None) -> Optional[D]:
        if dt is None:
            dt = datetime.utcnow()
        period = campaign.aggregation_period(dt)
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
