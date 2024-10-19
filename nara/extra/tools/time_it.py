import asyncio
import time
from functools import wraps
from typing import Any, Callable
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def timeIt(func: Callable):
    """
    Decorator function to measure the execution time of a synchronous or asynchronous function.

    Example:
    .. code-block:: python
        @TimeIt
        def my_function():
            time.sleep(1)

        my_function()  # Output: Prints execution time.

    """
    if asyncio.iscoroutinefunction(func):
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = await func(*args, *kwargs)
            end_time = time.time()
            
            result_message = (
                f"- Execution time for '{func.__name__}' : {end_time - start_time:.6f} Seconds.  \n"
            )
            console.print(Markdown(result_message), style="bold magenta")

            return result
        return async_wrapper
    else:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            result_message = (
                f"- Execution time for '{func.__name__}' : {end_time - start_time:.6f} Seconds.  \n"
            )
            console.print(Markdown(result_message), style="bold magenta")
            
            return result

        return wrapper



if __name__ == "__main__":
    @timeIt
    def my_function():
        time.sleep(1)

    my_function()
    #  • Execution time for 'my_function' : 1.001963 Seconds.