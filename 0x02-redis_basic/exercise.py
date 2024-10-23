import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


if __name__ == "__main__":
    cache = Cache()
    key = cache.store("sample data")
    print(f"Stored data under key: {key}")
