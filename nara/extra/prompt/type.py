from typing import Callable, Any
from dataclasses import dataclass
from enum import Enum


class Role(Enum):
    system = "system"
    user = "user"
    assistant = "assistant"

@dataclass
class File:
    """
    File class for text files

    Args:
        path: str
        cache: bool = True
    Returns:
        str
    """
    path: str
    cache: bool = True
    @property
    def text(self) -> str:
        if not self.cache:
            with open(self.path, "rb") as f:
                return f.read().decode("utf-8")
        elif self.cache and isinstance(self.cache, bool):
            with open(self.path, "rb") as f:
                self.cache = f.read().decode("utf-8")
        return self.cache

@dataclass
class Text:
    text: str

@dataclass
class Image:
    """
    Image class for images

    Args:
        text: str
        url: str
    """
    text: str
    url: str

class Function:
    """
    Function class for functions

    Args:
        func: Callable
        args: Any
        kwargs: Any

    Returns:
        Any
    
    Example:

    .. code-block:: python

        x = Function(slow_function_1, 1, 2)
        print(x())
    """
    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self) -> Any:
        return self.func(*self.args, **self.kwargs)