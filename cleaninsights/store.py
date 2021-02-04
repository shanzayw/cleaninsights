from typing import Dict
from typing import List
from typing import Union


class Store:
    events: List[Dict[str, Union[str, int, float]]]
    visits: List[Dict[str, Union[str, int, float]]]
