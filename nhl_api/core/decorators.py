import logging
from functools import wraps
from time import time
from typing import Callable

logger = logging.getLogger(__name__)


def timing(func: Callable):
    """
    Logs how long it takes for some function/method to run.

    :param func: the function we want to time
    :return: nested timer function
    """

    @wraps(func)
    def run_timer(*args, **kwargs):
        current_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        time_to_run = round(end_time - current_time, 4)
        logger.info(f"{func.__name__} took {time_to_run} seconds to run")
        return result

    return run_timer
