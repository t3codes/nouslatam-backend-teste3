from typing import Any, Optional
from time import time
import redis
import json

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

class CacheHandler:
    @staticmethod
    def set_cache(key: str, value: Any, ttl: int = 3600) -> None:
        redis_client.setex(key, ttl, json.dumps(value))

    @staticmethod
    def get_cache(key: str) -> Optional[Any]:
        cached_value = redis_client.get(key)
        if cached_value:
            return json.loads(cached_value)
        return None
