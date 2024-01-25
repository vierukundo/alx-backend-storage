#!/usr/bin/env python3
"""Writing strings to Redis"""
from typing import Union, Callable, Any
from functools import wraps
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a class method."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """Wrapper function that increments a key in Redis for Cache.store"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    """decorator to store the history of inputs
    and outputs for a particular function."""
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """method that records input and output data in Redis lists."""
        input_data = str(args)
        self._redis.rpush(input_key, input_data)
        output_data = method(self, *args)
        self._redis.rpush(output_key, output_data)
        return output_data

    return wrapper

def replay(method: Callable) -> None:
    """Print replay information for the given method."""
    class_name = method.__self__.__class__.__name__
    method_name = method.__name__
    qualified_name = method.__qualname__
    input_key = f"{qualified_name}:inputs"
    output_key = f"{qualified_name}:outputs"

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    num_calls = len(inputs)

    print(f"{qualified_name} from class {class_name} and method {method_name} was called {num_calls} times:")

    for inp, out in zip(inputs, outputs):
        input_str = inp.decode("utf-8")
        output_str = out.decode("utf-8")
        print(f"{qualified_name}(*{input_str}) -> {output_str}")

class Cache:
    """Representation of the Cache"""
    def __init__(self):
        """Initialization of class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store method"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """function that retrieves data from redis"""
        data = self._redis.get(key)
        if fn and data:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Retrieve a string from the cache using the specified key."""
        return str(self._redis.get(key))

    def get_int(self, key: str) -> int:
        """Retrieve an integer from the cache using the specified key."""
        return int(self._redis.get(key))
