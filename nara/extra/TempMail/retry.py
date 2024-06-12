import time
from functools import wraps
from typing import Callable, Any
from time import sleep
from rich import print

def retry(retries: int = 3, delay: float = 1) -> Callable:
    """
    Attempt to call a function, if it fails, try again with a specified delay.

    :param retries: The max amount of retries you want for the function call
    :param delay: The delay (in seconds) between each function retry
    :return:
    """

    # Don't let the user use this decorator if they are high
    if retries < 1 or delay <= 0:
        raise ValueError('Are you high, mate?')

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for i in range(1, retries + 1):  # 1 to retries + 1 since upper bound is exclusive

                try:
                    # print(f'[bold red]Running ({i}): {func.__name__}()[/bold red]')
                    return func(*args, **kwargs)
                except Exception as e:
                    # Break out of the loop if the max amount of retries is exceeded
                    if i == retries:
                        print(f'[bold red]Error: {repr(e)}.[/bold red]')
                        print(f'[bold red]"{func.__name__}()" failed after {retries} retries try again later.[/bold red]')
                        break
                    else:
                        print(f'[bold red]Error: {repr(e)} -> Retrying...[/bold red]')
                        sleep(delay)  # Add a delay before running the next iteration

        return wrapper

    return decorator

