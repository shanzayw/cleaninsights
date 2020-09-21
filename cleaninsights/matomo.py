"""
URLs really do need to be actual URLs otherwise the events do not get tracked.
"""

from decimal import Decimal
from random import randint
from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional
from typing import TypeVar
from urllib.parse import urlencode

import requests

Number = TypeVar('Number', int, float, Decimal)
LinkType = TypeVar('LinkType', Literal['link'], Literal['download'])

def generate_random_visitor_id() -> str:
    """Generates a random 16-character hex value to be used as a visitor ID."""
    return hex(randint(0, (2**64)-1))[2:].replace('L', '')

class Tracker:
    """Doesn't include things that scan or manipulate DOM, or the heart beat
    timer."""

    tracker_url: str
    site_id: int
    visitor_id: str
    token_auth: str

    API_VERSION: str = "1"

    def __init__(self, tracker_url: str, site_id: int,
                 visitor_id: Optional[str] = None,
                 token_auth: Optional[str] = None):
        if not tracker_url.endswith('?'):
            raise ValueError('tracker_url must be a full URL including trailing'
                             '"matomo.php?"')
        self.tracker_url = tracker_url
        self.site_id = site_id
        self.token_auth = "cd664e6b21a292b6b1bbc460619eff8e"
        # TODO: self.token_auth = token_auth

    def _build_url(self, params: Dict[str, Any]):
        params['apiv'] = 1
        params['rec'] = 1
        params['idsite'] = self.site_id
        if self.visitor_id is not None:
            params['_id'] = self.visitor_id
        if self.token_auth is not None:
            params['token_auth'] = self.token_auth
        # By default Matomo will try to extract the following from the
        # request, but that would be meaningless coming from the middleware.
        if 'cip' not in params:
            params['cip'] = '0.0.0.0'
        if 'ua' not in params:
            params['ua'] = 'Unknown'
        return self.tracker_url + urlencode(params)

    def track_page_view(self, url: Optional[str] = None,
                        custom_title: Optional[str] = None) -> str:
        """Return a URL to log a page view."""
        params: Dict[str, Any] = dict()
        if url:
            params['url'] = url
        if custom_title:
            params['action_name'] = custom_title
        return self._build_url(params)

    def track_event(self, category: str, action: str,
                    name: Optional[str] = None,
                    value: Optional[Number] = None) -> str:
        """Return a URL to log an event.

        Events have a category (e.g. Videos, Music, Games), an
        action (Play, Pause, Duration, Add Playlist, Downloaded,
        Clicked), an optional name and optional numeric value.
        """
        params: Dict[str, Any] = {
            'e_c': category.strip(),
            'e_a': action.strip(),
        }
        if name:
            params['e_n'] = name.strip()
        if value:
            params['e_v'] = value
        return self._build_url(params)

    def track_site_search(self, keyword: str, category: Optional[str] = None,
                          results_count: Optional[str] = None,
                          url: Optional[str] = None) -> str:
        """Return a URL to log an internal site search.

        A search is recorded for a specific keyword, in an optional
        category, specifying the optional count of search results in the
        page.
        """
        params: Dict[str, Any] = {
            'search': keyword,
        }
        if category:
            params['search_cat'] = category
        if results_count is not None:
            params['search_count'] = results_count
        if url:
            params['url'] = url
        return self._build_url(params)

    def track_goal(self, id_goal: int,
                   custom_revenue: Optional[Number]) -> str:
        """Log a conversion for the numeric goal ID, with an optional numeric
        custom revenue custom_revenue."""
        params: Dict[str, Any] = {
            'idgoal': id_goal,
        }
        if custom_revenue is not None:
            params['revenue'] = custom_revenue
        return self._build_url(params)

    def track_link(self, url: str, link_type: LinkType) -> str:
        """Log a click from your own code. url is the full URL which is to be
        tracked as a click. linkType can either be 'link' for an outlink or
        'download' for a download."""
        params: Dict[str, Any] = {
            'url': url,
        }
        if link_type == "download":
            params['download'] = url
        elif link_type == "link":
            params['link'] = url
        else:
            raise ValueError('link_type must be "download" or "link"')
        return self._build_url(params)

    def track_content_impression(self, content_name: str, content_piece: str,
                                 content_target: str) -> str:
        """Track a content impression using the specified values."""
        params: Dict[str, Any] = {
            'c_n': content_name,
            'c_p': content_piece,
            'c_t': content_target,
        }
        return self._build_url(params)

    def track_content_interaction(self, content_interaction: str,
                                  content_name: str, content_piece: str,
                                  content_target: str) -> str:
        """Track a content interaction using the specified values."""
        params: Dict[str, Any] = {
            'c_n': content_name,
            'c_p': content_piece,
            'c_t': content_target,
            'c_i': content_interaction,
        }
        return self._build_url(params)

    def ping(self) -> str:
        """Send a ping request.

        Ping requests do not track new actions. If they are sent within the
        standard visit length, they will extend the existing visit and the
        current last action for the visit. If sent after the standard visit
        length, ping requests will create a new visit using the last action in
        the last known visit. See also enableHeartBeatTimer.
        """
        params: Dict[str, Any] = {'ping': 1}
        return self._build_url(params)

class RequestsTracker:
    tracker: Tracker

    def __init__(self, tracker_url: str, site_id: int,
                 visitor_id: Optional[str] = None):
        self.tracker = Tracker(tracker_url, site_id, visitor_id)

    def __getattr__(self, attr):
        if not (attr.startswith("track_") or attr in ["ping"]):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{attr}'")
        else:
            def make_request(*args, **kwargs):
                api_url = self.tracker.__getattribute__(attr)(*args, **kwargs)
                r = requests.get(api_url)
                print(r.content)
            return make_request

    @property
    def tracker_url(self):
        return self.tracker.tracker_url

    @tracker_url.setter
    def tracker_url(self, value):
        self.tracker.tracker_url = value

    @property
    def site_id(self):
        return self.tracker.site_id

    @site_id.setter
    def site_id(self, value):
        self.tracker.site_id = value

    @property
    def visitor_id(self):
        return self.tracker.visitor_id

    @visitor_id.setter
    def visitor_id(self, value):
        self.tracker.visitor_id = value
