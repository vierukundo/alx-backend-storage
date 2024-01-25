#!/usr/bin/env python3
"""Writing strings to Redis"""
from typing import Union, Callable
import redis
import uuid


class Cache:
    """Representation of the Cache"""
    def __init__(self):
        """Initialization of class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
