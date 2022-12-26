from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Optional, Type

import pandas as pd

from nhl_api_py.core.utils import convert_keys_to_snake_case

logger = logging.getLogger(__name__)


@dataclass
class Model(ABC):
    """
    Base class that all Models from the NHL API are based off of.
    """

    @abstractmethod
    def from_dict(cls, data: dict):  # pragma: no cover
        """
        Helper function which performs removes specific keywords / fields
        from the response data depending on the Model.
        It preserves the dataclass' `__init__` method, making initialization
        easier for all subclasses.

        This should be called rather than the model's `__init__` method.
        This is because this method will account for possible data fields that may be
        included from some response data, that is not accounted for in models.
        Additionally, it replaces all camelCase fields to snake_case.

        :param data: dictionary containing all the data (e.g. the response data)
        :return: an instance of the model
        """
        raise NotImplementedError

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


@dataclass
class Play(Model):
    """
    Represents and contains all data for a single play from an NHL game.
    """

    players: Optional[list] = None
    event: Optional[str] = None
    event_type_id: Optional[str] = None
    description: Optional[str] = None
    secondary_type: Optional[str] = None
    strength_name: Optional[str] = None
    game_winning_goal: Optional[bool] = None
    empty_net: Optional[bool] = None
    penalty_severity: Optional[str] = None
    penalty_minutes: Optional[str] = None
    period: Optional[int] = None
    period_type: Optional[str] = None
    ordinal_num: Optional[str] = None
    period_time: Optional[str] = None
    period_time_remaining: Optional[str] = None
    date_time: Optional[str] = None
    goals_away: Optional[int] = None
    goals_home: Optional[int] = None
    coordinates: Optional[dict] = None
    team: Optional[Team] = None

    @classmethod
    def from_dict(cls, data: dict):
        converted_data = convert_keys_to_snake_case(data)
        # Extract nested data after top-level if it exists
        top_level_data = _field_only_keys(converted_data, cls)
        result_data = _field_only_keys(converted_data.get("result", dict()), cls)
        about_data = _field_only_keys(converted_data.get("about", dict()), cls)
        team_data = _field_only_keys(converted_data.get("team", dict()), Team)
        team_data = Team.from_dict(team_data) if len(team_data) != 0 else None
        final_data = {
            **top_level_data,
            **result_data,
            **about_data,
            "team": team_data,
        }
        return cls(**final_data)


@dataclass
class Game(Model):
    """
    Represents and contains all data for a given game, returned from the NHL API.
    """

    pk: Optional[int] = None
    season: Optional[str] = None
    type: Optional[str] = None
    date_time: Optional[str] = None
    end_date_time: Optional[str] = None
    abstract_game_state: Optional[str] = None
    coded_game_state: Optional[str] = None
    detailed_state: Optional[str] = None
    status_code: Optional[str] = None
    start_time_tbd: Optional[bool] = None
    away: Optional[Team] = None
    home: Optional[Team] = None
    players: Optional[dict] = None
    venue: Optional[dict] = None
    all_plays: Optional[list[Play]] = None
    scoring_plays: Optional[list] = None
    penalty_plays: Optional[list] = None
    plays_by_period: Optional[list] = None
    current_play: Optional[Play] = None
    decisions: Optional[dict] = None

    @classmethod
    def from_dict(cls, data: dict):
        converted_data = convert_keys_to_snake_case(data)
        game_data = converted_data.get("game_data", dict())
        live_data = converted_data.get("live_data", dict())
        top_level_game_data = _field_only_keys(game_data, cls)
        top_level_live_data = _field_only_keys(live_data, cls)
        game = _field_only_keys(game_data.get("game", dict()), cls)
        datetime_data = _field_only_keys(game_data.get("datetime", dict()), cls)
        status_data = _field_only_keys(game_data.get("status", dict()), cls)
        teams_data = _field_only_keys(game_data.get("teams", dict()), cls)
        away_data = _field_only_keys(teams_data.get("away", dict()), Team)
        away_data = Team.from_dict(away_data) if len(away_data) != 0 else None
        home_data = _field_only_keys(teams_data.get("home", dict()), Team)
        home_data = Team.from_dict(home_data) if len(home_data) != 0 else None
        play_data = live_data.get("plays", dict())
        play_data_kwargs = play_data.pop("all_plays", dict())
        all_plays = [
            Play.from_dict(play) if play_data_kwargs is not None else None
            for play in play_data_kwargs
        ]
        all_plays = None if all_plays == [] else all_plays
        current_play = play_data.get("current_play", dict())
        current_play = Play.from_dict(current_play) if current_play != dict() else None
        final_data = {
            **top_level_game_data,
            **top_level_live_data,
            **game,
            **datetime_data,
            **status_data,
            **play_data,
            "away": away_data,
            "home": home_data,
            "all_plays": all_plays,
            "current_play": current_play,
        }
        return cls(**final_data)


@dataclass
class Boxscore(Model):
    """
    Represents and contains boxscore data for a given game, returned from the NHL API.
    """

    away_team: Optional[Team] = None
    away_team_stats: Optional[dict] = None
    away_players: Optional[dict] = None
    away_goalies: Optional[list] = None
    away_skaters: Optional[list] = None
    away_on_ice: Optional[list] = None
    away_on_ice_plus: Optional[list] = None
    away_scratchers: Optional[list] = None
    away_penalty_box: Optional[list] = None
    away_coaches: Optional[list] = None
    home_team: Optional[Team] = None
    home_team_stats: Optional[dict] = None
    home_players: Optional[dict] = None
    home_goalies: Optional[list] = None
    home_skaters: Optional[list] = None
    home_on_ice: Optional[list] = None
    home_on_ice_plus: Optional[list] = None
    home_scratchers: Optional[list] = None
    home_penalty_box: Optional[list] = None
    home_coaches: Optional[list] = None
    officials: Optional[dict] = None

    @classmethod
    def from_dict(cls, data: dict):
        converted_data = convert_keys_to_snake_case(data)
        top_level_data = _field_only_keys(converted_data, cls)
        teams_data = converted_data.get("teams", dict())
        away_data = teams_data.get("away", dict())
        home_data = teams_data.get("home", dict())
        away_data_kwargs = away_data.pop("team", dict())
        home_data_kwargs = home_data.pop("team", dict())
        away_team = Team(**away_data_kwargs) if away_data_kwargs != dict() else None
        home_team = Team(**home_data_kwargs) if home_data_kwargs != dict() else None
        away_data = _append_string_to_keys("away_", away_data)
        home_data = _append_string_to_keys("home_", home_data)
        away_data = _field_only_keys(away_data, cls)
        home_data = _field_only_keys(home_data, cls)
        final_data = {
            **top_level_data,
            **away_data,
            **home_data,
            "away_team": away_team,
            "home_team": home_team,
        }
        return cls(**final_data)


def _field_only_keys(data: dict, cls: Type[Model]) -> dict:
    """
    Helper function that extracts only the keys from a dictionary that is a
    field / attribute from a Model.

    :param data: the dictionary we want to observe
    :param cls: the Model we want to consider
    :return: the same dictionary with only the model's fields
    """
    return {k: v for k, v in data.items() if k in (field.name for field in fields(cls))}


def _append_string_to_keys(text: str, d: dict) -> dict:
    """
    Helper function which appends a string to the top level keys of a dictionary.

    :param text: the text you want to append
    :param d: the dictionary we want to convert keys for
    :return: the same dictionary with converted keys
    """
    # Keys are being changed, so loop over a copy of d instead of d itself.
    for key in list(d):
        new_key = text + key
        d[new_key] = d.pop(key)
    return d
