from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from cleaninsights.event import Event
from cleaninsights.visit import Visit


class Store:
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
             **kwargs) -> Optional[List[Dict[str, Union[str, int, float]]]]:
        if len(args) > 0 and args[0] == "memory":
            return dict()
        else:
            raise NotImplementedError

    def persist(self) -> None:
        raise NotImplementedError

    def send(self, data: str, server: str, timeout: int) -> bool:
        raise NotImplementedError
