"""
Tests the `nhl_api.core.decorators` module.
"""
from time import sleep

import pytest

from nhl_api_py.core.decorators import timing


def test_timing(caplog):
    new_func = timing(lambda: sleep(0.5))
    new_func()
    assert len(caplog.records) == 1


def test_timing_no_logging_on_exception(caplog):
    def raise_error():
        raise Exception()

    new_func = timing(raise_error)
    with pytest.raises(Exception):
        new_func()
    assert len(caplog.records) == 0
