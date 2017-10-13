from flask import Flask
import redis
from Config import parse

database_name = parse['database']['database_name']
app = Flask(__name__)

pool = redis.ConnectionPool()
redis_connection = redis.Redis(connection_pool=pool)

@app.route('/')
def get_ip():
    redis_connection = redis.Redis(connection_pool=pool)
    result = redis_connection.srandmember(database_name)
    return result
