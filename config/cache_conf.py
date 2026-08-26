import json
from typing import Any

import redis.asyncio as redis

from config.settings import settings


# Redis client.
if settings.redis_url:
    redis_client = redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_timeout=settings.redis_socket_timeout,
    )
else:
    redis_client = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password,
        decode_responses=True,
        socket_timeout=settings.redis_socket_timeout,
    )


# Read a string value.
async def get_cache(key: str):
    # return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"Failed to get cache: {e}")
        return None


# Read a JSON value.
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"Failed to get JSON cache: {e}")
        return None


# Set cache with an expiration.
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"Failed to set cache: {e}")
        return False
