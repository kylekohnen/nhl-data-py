from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from nhl_api_py.core.utils import convert_keys_to_snake_case
from nhl_api_py.models.base import Model, _field_only_keys

logger = logging.getLogger(__name__)


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
    team_stats: Optional[dict] = None
    roster: Optional[dict] = None
    short_name: Optional[str] = None
    official_site_url: Optional[str] = None
    franchise_id: Optional[int] = None
    active: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict):
        converted_data = convert_keys_to_snake_case(data)
        return cls(**_field_only_keys(converted_data, cls))
