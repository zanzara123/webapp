from redis.asyncio import Redis

from settings import Settings

def get_redis_connection() -> Redis:
    settings = Settings()
    return Redis(
        host = settings.CACHE_HOST,
        port = settings.CACHE_PORT,
        db   = settings.CACHE_DB,
        decode_responses=True
    )