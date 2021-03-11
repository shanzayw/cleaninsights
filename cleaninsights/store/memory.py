from typing import Dict
from typing import List
from typing import Union

from cleaninsights.event import Event
from cleaninsights.store import Store
from cleaninsights.visit import Visit


class MemoryStore(Store):
    """A memory-resident store with no persistence."""

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
        """
        This class provides no persistence and so this function returns no data.
        """
        return dict()

    def persist(self) -> None:
        """
        This class provides no persistence and so this function does nothing.
        """
        pass
