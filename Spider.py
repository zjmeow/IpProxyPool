import requests
import pyquery
import redis

# 调用Spider()会自动验证代理是否过期
# 如果proxies里的代理数量小于30则重新爬取数据
# 调用get_random_ip可以获得ip代理
class Spider():
    def __init__(self):
        self.redis_pool = redis.ConnectionPool()
        self.proxy_pool_name = "proxies"

    def get_html(self, page=1, try_time=2):
        # 设置请求头
        url = 'http://www.xicidaili.com/nn/' + str(page)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        try:
            re = requests.get(url, headers=headers)
        except Exception:
            if try_time > 0:
                return self.get_html(url, try_time - 1)
            print('网页:', url, '抓取失败')
            return None
        else:
            return re.text

    # 从网页中解析出ip地址，返回ip列表
    def parse(self, html):
        l = []
        result = []
        soup = pyquery.PyQuery(html)
        ip = soup('.odd td:nth-child(2)')
        port = soup('.odd td:nth-child(3)')
        type = soup('.odd td:nth-child(6)')

        for (i, j) in zip(ip.items(), port.items()):
            l.append(i.text() + ':' + j.text())

        for (tp, i) in zip(type.items(), l):
            if (tp.text() != 'https'):
                result.append(i)

        return result

    # 验证ip是否有效
    def verify(self, ip):
        proxy = {'http': ip}
        try:
            response = requests.get('https://www.baidu.com/')
        except Exception:
            print('ip ', ip, 'is invalid')
            return False
        else:
            return True

    def __call__(self):
        redis_connection = redis.Redis(connection_pool=self.redis_pool)
        proxies = redis_connection.smembers(self.proxy_pool_name)
        pipe = redis_connection.pipeline(transaction=True)
        # 开始验证当前的ip代理是否有效
        for each in proxies:
            if (not self.verify(each)):
                redis_connection.smove(self.proxy_pool_name, "dst", each)
        i = 1
        while redis_connection.scard(self.proxy_pool_name) < 10:
            l = self.parse(self.get_html(page=i))
            for each in l:
                if (self.verify(each)):
                    redis_connection.sadd(self.proxy_pool_name, each)
        pipe.execute()



    def get_random_ip(self):
        redis_connection = redis.Redis(connection_pool=self.redis_pool)
        result = redis_connection.srandmember(self.proxy_pool_name)
        return result

s = Spider()
s()
redis_connection = redis.Redis(connection_pool=s.redis_pool)
proxies = redis_connection.smembers(s.proxy_pool_name)

# 开始验证当前的ip代理是否有效
for each in proxies:
    print(each)
