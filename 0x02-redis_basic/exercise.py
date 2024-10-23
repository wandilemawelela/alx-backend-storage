import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"{method.__qualname__}_calls"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str, int, bytes, float]]] = None) -> Optional[Union[str, int, bytes, float]]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value

    # Additional tests for get_str and get_int
    key_str = cache.store("hello")
    assert cache.get_str(key_str) == "hello"

    key_int = cache.store(42)
    assert cache.get_int(key_int) == 42

    # Check if count_calls is working
    print(f"store method called {cache._redis.get('Cache.store_calls').decode('utf-8')} times")

    print("All tests passed.")
