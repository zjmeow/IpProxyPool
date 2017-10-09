from flask import Flask
from Spider import Spider

app = Flask(__name__)
spider = Spider()
spider()


@app.route('/')
def get_ip():
    return spider.get_random_ip()


app.run()
