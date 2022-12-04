from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class Model(ABC):
    """
    Base class that all Models from the NHL API are based off of.
    """


@dataclass
class Team(Model):
    """
    Represents and contains all data for a single team, returned from the NHL API.
    """

    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None
    venue: Optional[dict] = None
    abbreviation: Optional[str] = None
    team_name: Optional[str] = None
    location_name: Optional[str] = None
    first_year_of_play: Optional[int] = None
    division: Optional[dict] = None
    conference: Optional[dict] = None
    franchise: Optional[dict] = None
    team_status: Optional[dict] = None
    roster: Optional[dict] = None
    short_name: Optional[str] = None
    official_site_url: Optional[str] = None
    franchise_id: Optional[int] = None
    active: Optional[bool] = None
