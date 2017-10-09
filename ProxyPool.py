from flask import Flask
import redis

app = Flask(__name__)

pool = redis.ConnectionPool()
redis_connection = redis.Redis(connection_pool=pool)

@app.route('/')
def get_ip():
    redis_connection = redis.Redis(connection_pool=pool)
    result = redis_connection.srandmember("proxies")

    return result

app.run()
