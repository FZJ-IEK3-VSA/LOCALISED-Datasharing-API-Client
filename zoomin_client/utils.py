import time
from functools import wraps
from typing import Any, Callable
import logging

utils_log = logging.getLogger("utils")
logging.basicConfig(level=logging.INFO)


def measure_time(func_call: Callable) -> Any:
    """Wrap around a function to track the time taken by the function.

    :param func: Function

    .. note:: Usage as a decorator before a function -> @timer

    """

    @wraps(
        func_call
    )  # Required to get documentation for functions using this decorator
    def _f(*args: Any, **kwargs: Any) -> Any:
        before = time.perf_counter()
        r_v = func_call(*args, **kwargs)
        after = time.perf_counter()

        time_taken = round((after - before) / 60, 2)
        utils_log.info(f"Elapsed time for {func_call}: {time_taken} minutes")
        return r_v

    return _f
