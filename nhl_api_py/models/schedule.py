from __future__ import annotations

from dataclasses import dataclass

from nhl_api_py.core.models import Model


@dataclass
class ScheduleDate(Model):
    date: str
    total_items: int
    total_events: int
    total_games: int
    total_matches: int
    games: list
    events: list
    matches: list


@classmethod
def from_dict(cls, data: dict):
    pass
