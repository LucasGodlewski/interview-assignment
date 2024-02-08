from datetime import datetime
from datetime import timedelta
from functools import lru_cache, wraps

from config import DEBUG


def timed_lru_cache(seconds: int, maxsize: int):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                if DEBUG:
                    print(f'LRU Cache stats: {func.cache_info()}')
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
