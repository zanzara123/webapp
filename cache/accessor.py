import redis

def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host= "localhost",
        port=6379,
        db=0
    )

def set_value():
    redis = get_redis_connection()
    redis.set(name="цена", value=1) #ex - время жизни в секундах