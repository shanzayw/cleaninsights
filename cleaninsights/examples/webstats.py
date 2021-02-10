import argparse
import sys
from datetime import MAXYEAR
from datetime import date

from cleaninsights.campaign import Campaign
#from cleaninsights.memory import MemoryStore
from cleaninsights.conf import Configuration
from cleaninsights import CleanInsights

def parse_args():
    parser = argparse.ArgumentParser(description="Import webstats logs.")
    parser.add_argument('logs', nargs='*', type=argparse.FileType('r'),
                        default=[sys.stdin])
    return parser.parse_args()

def ci_init():
    campaign  = Campaign.from_dict({
        "aggregation_period_length": 7,
        "end": date(MAXYEAR, 12, 31),
        "event_aggregation_rule": "sum",
        "only_record_once": False,
        "start": date(1970, 1, 5)
    })
    config = Configuration.from_dict({
        "campaigns": [campaign],
        "debug": False,
        "persist_every_n_times": 1,
        "server": "metrics.cleaninsights.org",
        "site_id": 4,
        "server_side_anon_usage": True,
        "timeout": 10
    })
    store = MemoryStore()
    ci = CleanInsights(config, store)

def run():
    args = parse_args()
    ci = ci_init()
    for f in args.logs:
        print(f)

if __name__ == "__main__":
    run()
