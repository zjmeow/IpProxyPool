# encoding:utf-8
import redis

pool = redis.ConnectionPool()
r = redis.Redis(connection_pool=pool)
pipe = r.pipeline(transaction=True)
r.sadd("1", 1, 2, 3)
pipe.execute()
for each in r.smembers("1"):
    print(int(each))