import copy
import random
import time
from flask import Flask
from flask_uwsgi_websocket import WebSocket

app = Flask(__name__)
sockets = WebSocket(app)

def get_price(old_price, volatility=0.02):
    change_percent = volatility * (random.random() - .5)
    return max(old_price + old_price * change_percent, 0)

@app.route("/")
def main():
    return "Get a stream of stock prices from <code>ws://54.196.193.22/stock</code>"

@sockets.route('/stock')
def echo_socket(socket):
    price = get_price(100)
    while True:
        time.sleep(.2)
        oldprice = price
        price = get_price(price)
        socket.send('${0:.2f} {1:+.2f}'.format(price, price - oldprice))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

