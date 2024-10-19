import json
import os
from functools import wraps
from rich import print as rprint

class CacheManager:
    """
    A class for managing function result caching to disk.

    This class provides functionality to cache the results of functions to disk, allowing for faster
    retrieval of previously computed results. It maintains an in-memory cache dictionary and provides
    methods to load, save, and cache function results.

    Parameters
    ----------
    filename : str
        The name of the file to store the cache data.

    Attributes
    ----------
    filename : str
        The name of the file to store the cache data.
    cache_data : dict
        The in-memory cache dictionary containing cached function results.

    Methods
    -------
    loadCache():
        Load cached data from the specified file.
    saveCache():
        Save the in-memory cache data to the specified file.
    cache(func):
        Decorator function to cache the results of the decorated function.

    Examples
    --------
    >>> cache_manager = CacheManager("cache.json")
    >>> 
    >>> @cache_manager.cache
    ... def my_function(x, y):
    ...     return x + y
    >>> 
    >>> result = my_function(3, 4)
    >>> print(result)  # Output: 7

    This class allows for efficient caching of function results to disk, reducing computation time for
    frequently called functions.
    """

    def __init__(self, filename):
        """
        Initialize the CacheManager with the specified filename.

        Parameters
        ----------
        filename : str
            The name of the file to store the cache data.
        """
        self.filename = filename
        self.cache_data = {}
        self.loadCache()

    def loadCache(self):
        """
        Load cached data from the specified file.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    self.cache_data = json.load(file)
                except json.JSONDecodeError:
                    self.cache_data = {}
        else:
            self.cache_data = {}

    def saveCache(self):
        """
        Save the in-memory cache data to the specified file.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.cache_data, file, indent=2)

    def cache(self, func):
        """
        Decorator function to cache the results of the decorated function.

        Parameters
        ----------
        func : function
            The function to be decorated for caching.

        Returns
        -------
        function
            The decorated function with caching functionality.

        Notes
        -----
        This decorator works by storing the function arguments and result in a dictionary. If the same
        set of arguments is passed to the function again, the cached result is returned instead of
        recomputing the function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Normalize the key
            key = f"{func.__name__}:{args}:{kwargs}"

            # Check if the key exists in the in-memory cache
            if key in self.cache_data:
                rprint("[bold green]Returning cached result.[/bold green]")
                return self.cache_data[key]
            else:
                # Compute the result
                result = func(*args, **kwargs)

                # Save the result to the in-memory cache
                self.cache_data[key] = result

                # Save the updated cache back to the file
                self.saveCache()

                return result

        return wrapper

if __name__ == "__main__":
    cache_manager = CacheManager("cache.json")
    from time import sleep
    @cache_manager.cache
    def my_function(x, y):
        sleep(5)
        print("sleeping")
        return x + y

    result = my_function(3, 4)
    print(result)