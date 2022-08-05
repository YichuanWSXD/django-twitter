import redis

from twitter import settings


class RedisClient:
     conn = None

     @classmethod
     def get_connection(cls):
         # singleton
        if cls.conn:
            return cls.conn
        cls.conn = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
         )
        return cls.conn

     @classmethod
     def clear(cls):
         if not settings.TESTING:
             raise Exception("You can't flush redis in production environment")
         conn = cls.get_connection()
         conn.flushdb()