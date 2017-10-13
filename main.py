import Spider
import time
import threading
from ProxyPool import app
from Config import parse
from Spider import Spider

# parse为从config中读取出的参数
host = parse['pool']['host']
port = parse['pool']['port']
database_name = parse['database']['database_name']
sleep_time = parse['spider']['sleep_time']
s = Spider(database_name)


# 定时获取
def get_ip():
    while True:
        s()
        time.sleep(sleep_time)


thread = threading.Thread(target=get_ip())
app.run(host=host, port=port)
