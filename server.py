from flask import Flask
from flask import request
from market_operator import MarketOperator
from order_book import Order
from phe import paillier
from phe import EncryptedNumber

mop = MarketOperator()
app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	return '''
Encrypted order book: <a href="/order-book">/order-book</a> <br>
Plaintext order book (for debugging purposes): <a href="/raw-order-book">/raw-order-book</a> <br>
Trade history and proofs of correctness: <a href="/history">/history</a> <br>
Market operator public key: <a href="/public-key">/public-key</a> <br>
POST to <a href="/submit-order">/submit-order</a> to submit orders (see code for parameters)
'''

@app.route("/submit-order",  methods=['POST'])
def submit_order():
	price_ciphertext = request.values.get('encrypted_price', type=int)
	qty_ciphertext = request.values.get('encrypted_qty', type=int)
	price_nonce = request.values.get('price_nonce', type=int)
	qty_nonce = request.values.get('qty_nonce', type=int)
	direction = request.values.get('direction', type=str)

	assert direction in {'ask', 'bid'}

	if direction == "ask":
		mop.submit_ask(price_ciphertext, qty_ciphertext, price_nonce, qty_nonce)

	if direction == "bid":
		mop.submit_bid(price_ciphertext, qty_ciphertext, price_nonce, qty_nonce)

	return "submitting order"

@app.route("/order-book", methods=['GET'])
def order_book():
	return mop.get_encrypted_book().replace('\n', '<br>')

@app.route("/raw-order-book", methods=['GET'])
def raw_order_book():
	return mop.get_unencrypted_book().replace('\n', '<br>')

@app.route("/history", methods=['GET'])
def history():
	return mop.get_history().replace('\n', '<br>')

@app.route("/public-key", methods=['GET'])
def public_key():
	return mop.get_public_key()


if __name__ == "__main__":
	app.run()
