from flask import Flask
from flask import request
from market_operator import MarketOperator
from order_book import Order


mop = MarketOperator()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	return order_book()

@app.route("/submit-order",  methods=['POST'])
def submit_order():
	price = request.values.get('price', type=float)
	quantity = request.values.get('quantity', type=int)
	direction = request.values.get('direction', type=str)
	
	assert direction in {'ask', 'bid'}, "direction invalid"
	assert quantity > 0, "quantity invalid"
	assert price > 0, "price invalid"

	if direction == "ask":
		mop.submit_ask(price, quantity)
	if direction == "bid":
		mop.submit_bid(price, quantity)
	return "Submitting order"

@app.route("/bulletin", methods=['GET'])
def bulletin():
	return mop.bulletin

@app.route("/order-book", methods=['GET'])
def order_book():
	return mop.get_encrypted_book()
	
@app.route("/history", methods=['GET'])
def history():
	return mop.get_history()


if __name__ == "__main__":
	app.run()
