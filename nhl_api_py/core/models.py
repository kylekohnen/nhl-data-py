from __future__ import annotations

import logging
from abc import ABC
from dataclasses import dataclass, fields
from typing import Optional

import pandas as pd

from nhl_api_py.core.utils import camel_to_snake_case, flatten_dictionary

logger = logging.getLogger(__name__)


@dataclass
class Model(ABC):
    """
    Base class that all Models from the NHL API are based off of.
    """

    @classmethod
    def from_kwargs(cls, **kwargs):
        """
        Helper function which performs removes specific keywords / fields
        from the response data depending on the Model.
        It preserves the dataclass' `__init__` method, making initialization
        easier for all subclasses.

        This should be called rather than the model's `__init__` method.
        This is because this method will account for possible data fields that may be
        included from some response data, that is not accounted for in models.
        Additionally, it replaces all camelCase fields to snake_case.

        :return: an instance of the model
        """
        kwargs = dict(flatten_dictionary(kwargs), **kwargs)
        kwargs = {camel_to_snake_case(key): value for key, value in kwargs.items()}
        included_keys = [
            key for key in kwargs if key in (field.name for field in fields(cls))
        ]
        keys_not_defined = [key for key in kwargs if key not in included_keys]
        if len(keys_not_defined) > 0:
            logger.warning(
                "The following arguments were included in the response data "
                + f"but are being excluded: {keys_not_defined}"
            )
        return cls(**{k: v for k, v in kwargs.items() if k in included_keys})

    def to_series(self, remove_missing_values: bool = True) -> pd.Series:
        """
        Convenience method which generates a pandas Series from the dataclass.

        :param remove_missing_values: whether missing values should be
            kept in the series, defaults to True
        :return: all attributes ordered in a pandas Series
        """
        column = pd.Series(self.__dict__)
        if remove_missing_values:
            column.dropna(inplace=True)
        return column


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


@dataclass
class Play(Model):
    """
    Represents and contains all data for a single play from an NHL game.
    """

    players: Optional[list] = None
    result_event: Optional[str] = None
    result_event_type_id: Optional[str] = None
    result_description: Optional[str] = None
    result_secondary_type: Optional[str] = None
    result_strength_name: Optional[str] = None
    result_game_winning_goal: Optional[bool] = None
    result_empty_net: Optional[bool] = None
    result_penalty_severity: Optional[str] = None
    result_penalty_minutes: Optional[str] = None
    about_period: Optional[int] = None
    about_period_type: Optional[str] = None
    about_ordinal_num: Optional[str] = None
    about_period_time: Optional[str] = None
    about_period_time_remaining: Optional[str] = None
    about_date_time: Optional[str] = None
    about_goals_away: Optional[int] = None
    about_goals_home: Optional[int] = None
    coordinates: Optional[dict] = None
    team: Optional[Team] = None

    @classmethod
    def from_kwargs(cls, **kwargs):
        play: Play = super().from_kwargs(**kwargs)
        # Turn Team Dict if its from a Response to a Team Model
        if isinstance(play.team, dict):
            team = play.team.copy()
            team["abbreviation"] = team.pop("triCode")
        play.team = Team.from_kwargs(**team) if isinstance(team, dict) else None
        return play
