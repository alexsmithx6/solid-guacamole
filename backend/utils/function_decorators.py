import os, sys
from loguru import logger
import functools
from typing import Callable, Any

def try_catch_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    '''
    A decorator function to log start/end of functions and log exceptions

    Usage:
    @try_catch_decorator
    def my_function():
        # Your code in here
    '''

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

        try:
            logger.debug(f'START {func.__name__} task in module: {func.__module__}')
            ret = func(*args, **kwargs)
            return 0, '', ret
        except Exception as exitMessage:
            logger.exception(f'Exception occurred in {func.__name__}: {exitMessage}')
            return 1, exitMessage, None
        finally:
            logger.debug(f'STOP {func.__name__} task in module: {func.__module__}')

    return wrapper

if __name__ == '__main__':
    @try_catch_decorator
    def add(x: int, y: int) -> int:
        return x + y

    print(add(3, 4))

    print(add('not an int', 4))