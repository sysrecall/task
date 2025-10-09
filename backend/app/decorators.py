import redis
from functools import wraps
import pickle
from typing import Any, Awaitable, Callable, List

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool, decode_responses=True)

def cache(expire_time: int, exclude_params: List[str] | None = None):
    if exclude_params is None:
        exclude_params = []

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cache_key_parts = [f"{func.__module__}.{func.__name__}"]

            func_arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]

            args_filtered = [
                arg for arg, name in zip(args, func_arg_names) 
                if name not in exclude_params
            ]
            kwargs_filtered = {k: v for k, v in kwargs.items() if k not in exclude_params}

            cache_key_parts.append(str(args_filtered))
            cache_key_parts.append(str(sorted(kwargs_filtered.items())))

            cache_key = ':'.join(cache_key_parts)
            print('args:', args)
            print('cache key:', cache_key)
            cached_result = r.get(cache_key)

            if isinstance(cached_result, Awaitable):
                cached_result = await cached_result

            if cached_result:
                print('cache hit!')
                return pickle.loads(cached_result)

            print('cache miss!')
            result = func(*args, **kwargs)

            r.set(cache_key, pickle.dumps(result), ex=expire_time)
            return result
            
        return wrapper
    return decorator
