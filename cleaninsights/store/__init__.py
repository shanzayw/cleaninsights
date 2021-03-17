import http.client
import json
from typing import Dict
from typing import List
from typing import Union
import urllib.parse

from cleaninsights.event import Event
from cleaninsights.visit import Visit


class InsightsEncoder(json.JSONEncoder):
    """A JSON encoder class for events and visits."""

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



class Store:
    """An abstract Store to be extended by specific implementations."""

    events: List[Event]
    visits: List[Visit]

    def __init__(self, *args, **kwargs):
        data = self.load(*args, **kwargs)
        if data is None:
            raise RuntimeError("Storage doesn't exist or isn't readable.")
        if 'events' in data:
            self.events = [Event(**e) for e in data['events']]
        else:
            self.events = []
        if 'visits' in data:
            self.visits = [Visit(**v) for v in data['visits']]
        else:
            self.visits = []

    def load(self, *args,
             **kwargs) -> Dict[str, List[Dict[str, Union[str, int, float]]]]:
        raise NotImplementedError

    def persist(self) -> None:
        raise NotImplementedError

    def send(self, data: str, server: str, timeout: int) -> bool:
        url = urllib.parse.urlparse(server)
        print(repr(url))
        conn = http.client.HTTPSConnection(url.netloc, timeout=timeout.total_seconds())
        headers = {"Content-Type": "application/json"}
        conn.request("POST", url.path, data.encode("utf-8"), headers)
        resp = conn.getresponse()
        if resp.status in ['200', '204']:
            return True
        else:
            return False

    def _generate_insights(self, site_id: int) -> Dict:
        # TODO: Ignore insights older than a certain date
        return json.dumps({
            "idsite": site_id,
            "visits": self.visits,
            "events": self.events
        }, cls=InsightsEncoder)