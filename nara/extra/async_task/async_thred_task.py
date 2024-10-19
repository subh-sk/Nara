import asyncio
from functools import wraps
import inspect
from concurrent.futures import ThreadPoolExecutor

def asyncThreadedTask(thread_count: int=1, *threading_args, **threading_kwargs):
    """
    Wraps an asynchronous function with a decorator that runs it in a separate thread.

    This decorator allows running an asynchronous function `func` in a thread-safe manner by 
    executing it in a single-threaded ThreadPoolExecutor. It removes any decorators applied 
    to `func` and then executes it asynchronously.

    Args:
        thread_count (int, optional): Number of threads in the ThreadPoolExecutor. Defaults to 1.
        *threading_args: Additional positional arguments for ThreadPoolExecutor.
        **threading_kwargs: Additional keyword arguments for ThreadPoolExecutor.

    Returns:
        callable: An async function wrapper that executes `func` in a separate thread.

    Raises:
        RuntimeError: If the function `func` is not asynchronous.

    Usage:
        .. code-block:: python
        @async_threaded_task
        async def async_function(*args, **kwargs):
            # Function body
        
        # Can also specify the number of threads to use for execution.
        @async_threaded_task(1)
        async def async_function(*args, **kwargs):
            # Function body
        
        async def main():
            await async_function()
        
        asyncio.run(main())

    Notes:
        - This decorator is useful for running async functions that need to be executed
        in a thread-safe manner, typically when interfacing with synchronous libraries
        or performing blocking I/O operations.

        - It assumes that decorators applied to `func` are written in standard form
        (`@decorator` above the function definition) and removes those lines from
        the source code before execution.
    """

    if callable(thread_count):  # If used without arguments as a decorator
        func = thread_count
        
        if not asyncio.iscoroutinefunction(func):
            raise RuntimeError("The function must be asynchronous.")

        @wraps(func)
        async def wrapper(*args, **kwargs):
            loop = asyncio.get_running_loop()
            source_lines, _ = inspect.getsourcelines(func)
            source_lines = [line for line in source_lines if not line.lstrip().startswith('@')]
            source_text = ''.join(source_lines)

            def wrap():
                local_vars = {}
                exec(source_text, func.__globals__, local_vars)
                new_func = local_vars[func.__name__]
                return asyncio.run(new_func(*args, **kwargs))  # Ensure the inner coroutine is awaited

            return await loop.run_in_executor(
                ThreadPoolExecutor(
                    max_workers=1,  # Default to 1 thread if not specified
                    *threading_args,
                    **threading_kwargs
                ),
                wrap
            )
        return wrapper
    
    else:  # If used with arguments
        def decorator(func):
            if not asyncio.iscoroutinefunction(func):
                raise RuntimeError("The function must be asynchronous.")

            @wraps(func)
            async def wrapper(*args, **kwargs):
                loop = asyncio.get_running_loop()
                source_lines, _ = inspect.getsourcelines(func)
                source_lines = [line for line in source_lines if not line.lstrip().startswith('@')]
                source_text = ''.join(source_lines)

                def wrap():
                    local_vars = {}
                    exec(source_text, func.__globals__, local_vars)
                    new_func = local_vars[func.__name__]
                    return asyncio.run(new_func(*args, **kwargs))  # Ensure the inner coroutine is awaited

                return await loop.run_in_executor(
                    ThreadPoolExecutor(
                        max_workers=thread_count,
                        *threading_args,
                        **threading_kwargs
                    ),
                    wrap
                )
            return wrapper
        return decorator