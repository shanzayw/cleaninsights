import argparse
import sys
from datetime import MAXYEAR
from datetime import date

from cleaninsights.store import Store
from cleaninsights.conf import Configuration
from cleaninsights import CleanInsights


def parse_args():
    parser = argparse.ArgumentParser(description="Import webstats logs.")
    parser.add_argument('logs',
                        nargs='*',
                        type=argparse.FileType('r'),
                        default=[sys.stdin])
    return parser.parse_args()


def ci_init():
    config = Configuration.from_dict({
        "debug": False,
        "persist_every_n_times": 1,
        "server": "metrics.cleaninsights.org",
        "server_side_anon_usage": True,
        "site_id": 4,
        "timeout": 10,
        "campaigns": [{
            "aggregation_period_length": 7,
            "end": date(MAXYEAR, 12, 31),
            "event_aggregation_rule": "sum",
            "only_record_once": False,
            "start": date(1970, 1, 5)
        }]
    })
    store = Store("memory")
    ci = CleanInsights(config, store)


def run():
    args = parse_args()
    ci = ci_init()
    for f in args.logs:
        print(f)


if __name__ == "__main__":
    run()
