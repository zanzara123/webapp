import redis

from settings import Settings

def get_redis_connection() -> redis.Redis:
    settings = Settings()
    return redis.Redis(
        host = Settings.CACHER_HOST,
        port = Settings.CACHER_PORT,
        db   = Settings.CACHER_DB
    )