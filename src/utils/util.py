from typing import Callable, TypeVar, ParamSpec
import threading
import functools

P = ParamSpec("P")
R = TypeVar("R")


def with_lock(lock: threading.Lock) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorator
