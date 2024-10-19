import asyncio
from functools import wraps


def runMultipleTimes(count: int=1):
    """
    A decorator to run an asynchronous function multiple times concurrently.

    This decorator schedules the decorated async function to run concurrently
    a specified number of times using asyncio.gather.

    Args:
        count (int): The number of times to run the decorated function concurrently.
                     Defaults to 1.

    Returns:
        Callable: The decorated async function that will run multiple times concurrently.

    Example:
    .. code-block:: python
        @runMultipleTimes(5)
        async def task_runner():
            await some_async_function()
        # This will run `task_runner` 5 times concurrently when called.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tasks = [func(*args, **kwargs) for _ in range(count)]
            await asyncio.gather(*tasks)
        return wrapper
    return decorator