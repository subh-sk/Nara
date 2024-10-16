import asyncio
import time
from functools import wraps
from typing import Optional
from humanfriendly import parse_timespan,InvalidTimespan


def repeat_forever(sleep_interval: Optional[float] = None, end_after: Optional[str] = None):
    """
    A decorator to repeatedly execute a function or coroutine function forever with an optional sleep interval between iterations,
    and an optional end time after which the repetition will stop.

    Parameters:
        sleep_interval (Optional[float]): Time in seconds to sleep between iterations. Defaults to None.
        end_after (Optional[str]): A human-friendly string representing the duration after which the repetition should stop.
                                   Uses the `humanfriendly` package to parse the string. Defaults to None.

    Returns:
        A function or coroutine function that will be executed repeatedly according to the specified parameters.
    
    Raises:
        InvalidTimespan: If the `end_after` string is not a valid timespan.

    Example Usage:
        .. code-block:: python
        @repeat_forever(sleep_interval=2.0, end_after="10 minutes")
        def print_message():
            print("Hello, World!")
        
        @repeat_forever(sleep_interval=1.0, end_after="5 minutes")
        async def async_print_message():
            print("Hello, Async World!")
    """
    def decorator(func):
        if end_after:
            try:
                end_after_seconds = parse_timespan(end_after)
            except:
                raise InvalidTimespan(f"Invalid timespan string: {end_after}")
        else:
            end_after_seconds = None

        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                while True:
                    await func(*args, **kwargs)
                    if sleep_interval:
                        await asyncio.sleep(sleep_interval)
                    if end_after_seconds and (time.time() - start_time) >= end_after_seconds:
                        break
            return async_wrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                while True:
                    func(*args, **kwargs)
                    if sleep_interval:
                        time.sleep(sleep_interval)
                    if end_after_seconds and (time.time() - start_time) >= end_after_seconds:
                        break
            return wrapper
    return decorator