from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

from nhl_api_py.core.utils import convert_keys_to_snake_case
from nhl_api_py.models.base import Model, _field_only_keys
from nhl_api_py.models.game import Game

logger = logging.getLogger(__name__)


@dataclass
class ScheduleDate(Model):
    date: Optional[str] = None
    total_items: int = 0
    total_events: int = 0
    total_games: int = 0
    total_matches: int = 0
    games: list = field(default_factory=list)
    events: list = field(default_factory=list)
    matches: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        converted_data = convert_keys_to_snake_case(data)
        games: list = converted_data.pop("games", [])
        top_level_data = _field_only_keys(converted_data, cls)
        final_data = {**top_level_data, "games": [Game(game) for game in games]}
        print(final_data)
        return cls(**final_data)
