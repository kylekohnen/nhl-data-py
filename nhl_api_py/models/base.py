from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Type

import pandas as pd

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
