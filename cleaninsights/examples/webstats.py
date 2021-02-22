import argparse
import json
import re
import sys
import time
from datetime import MAXYEAR
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from datetime import tzinfo
from io import TextIOWrapper
from typing import Iterator
from typing import Optional

from cleaninsights import CleanInsights
from cleaninsights.conf import Configuration
from cleaninsights.store import Store
from cleaninsights.visit import Visit

WEBSTATS_LINE_REGEX = (
    r"^((?:\d{1,3}\.){3}\d{1,3}) (\S+) (\S+) \[([\w/]+[\w:]+"
    r"\s[+\-]\d{4})\] \"([A-Z]+) ([^\"]+) ([A-Z]+/\d\.\d)\" "
    r"(\d{3}) (\d+|-)(.*)$")


class CleanInsightsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Visit):
            return {
                "action_name": obj.path,
                "times": obj.times,
                "period_start": obj.first,
                "period_end": obj.last
            }
        elif isinstance(obj, date):
            return time.mktime(obj.timetuple())
        else:
            return json.JSONEncoder.default(self, obj)


class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""
    def __init__(self, string):
        if string[0] == '-':
            direction = -1
            string = string[1:]
        elif string[0] == '+':
            direction = +1
            string = string[1:]
        else:
            direction = +1
            string = string

        hr_offset = int(string[0:2], 10)
        min_offset = int(string[2:3], 10)
        min_offset = hr_offset * 60 + min_offset
        min_offset = direction * min_offset

        self.__offset = timedelta(minutes=min_offset)

        self.__name = string

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return timedelta(0)

    def __repr__(self):
        return repr(self.__name)


def apache_date(s):
    """
    Parse a date from an Apache log file.
    Given a string representation of a datetime in apache format (e.g.
    "01/Sep/2012:06:05:11 +0000"), returns a UTC :class:`date <datetime.date>`
    for that string.
    """
    month_map = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    #s = s[1:-1]
    tz_string = s[21:26]
    tz = FixedOffset(tz_string)
    return datetime(year=int(s[7:11]),
                    month=month_map[s[3:6]],
                    day=int(s[0:2]),
                    hour=int(s[12:14]),
                    minute=int(s[15:17]),
                    second=int(s[18:20]),
                    tzinfo=tz).astimezone(timezone.utc)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Import webstats logs.")
    parser.add_argument('logs',
                        nargs='*',
                        type=argparse.FileType('r'),
                        default=[sys.stdin])
    return parser.parse_args()


def ci_init():
    """Initialize the CleanInsights SDK."""
    config = Configuration.from_dict({
        "debug": False,
        "persist_every_n_times": 1,
        "server": "metrics.cleaninsights.org",
        "server_side_anon_usage": True,
        "site_id": 4,
        "timeout": 10,
        "campaigns": {
            "webstats": {
                "aggregation_period_length": 7,
                "end": date(MAXYEAR, 12, 31),
                "event_aggregation_rule": "sum",
                "only_record_once": False,
                "start": date(1970, 1, 5)
            }
        }
    })
    store = Store("memory")
    return CleanInsights(config, store)


def parse_log(logfile: TextIOWrapper) -> Iterator[Optional[re.Match[str]]]:
    """Parse an Apache log file returning an iterator."""
    p = re.compile(WEBSTATS_LINE_REGEX)
    for line in logfile:
        yield p.match(line)


def run():
    """Run the webstats application."""
    args = parse_args()
    ci = ci_init()
    for logfile in args.logs:
        for line in parse_log(logfile):
            ci.measure_visit(line.group(6), "webstats", dt=apache_date(line.group(4)))
    print(
        json.dumps({
            "idsite": ci.conf.site_id,
            "visits": ci.store.visits
        }, cls=CleanInsightsEncoder))


if __name__ == "__main__":
    run()
