from dataclasses import dataclass
from datetime import timedelta
from typing import Any
from typing import Dict

from cleaninsights.campaign import Campaign


@dataclass
class Configuration:
    server: str
    site_id: int
    campaigns: Dict[str, Campaign]
    timeout: timedelta
    max_retry_delay: timedelta
    persist_every_n_times: int
    server_side_anon_usage: bool
    debug: bool

    @classmethod
    def from_dict(cls, conf_data: Dict[str, Any]):  # -> Configuration
        campaigns = {
            k: Campaign.from_dict(v)
            for (k, v) in conf_data["campaigns"].items()
        }
        return Configuration(conf_data["server"], conf_data["site_id"],
                             campaigns,
                             timedelta(seconds=conf_data["timeout"]),
                             timedelta(seconds=conf_data["max_retry_delay"]),
                             conf_data["persist_every_n_times"],
                             conf_data["server_side_anon_usage"],
                             conf_data["debug"])
