from flask import Flask
from flask import request
from market_operator import MarketOperator


mop = MarketOperator()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return "Hello World!"

@app.route("/submit-order",  methods=['POST'])
def submit_order():
    price = request.values.get('price', type=float)
    quantity = request.values.get('quantity', type=int)
    direction = request.values.get('direction', type=str)

    assert direction in {'ask', 'bid'}
    assert quantity > 0
    assert price > 0

    return "Submitting order"

@app.route("/bulletin", methods=['GET'])
def bulletin():
    return mop.bulletin

@app.route("/order-book", methods=['GET'])
def order_book():
    return mop.get_encrypted_book()


if __name__ == "__main__":
    app.run()
