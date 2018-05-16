from order_book import OrderBook
from order_book import Order

class MarketOperator:

	def __init__(self):
		self.book = OrderBook()
		self.next_id = 0
		self.bulletin = ''
		
	def get_public_key(self):
		return str(self.book.public_key.n)
		
	def get_encrypted_book(self):
		return self.book.get_encrypted_book()
		
	def get_unencrypted_book(self):
		return self.book.get_unencrypted_book()
		
	def submit_bid(self, price_ciphertext, qty_ciphertext, price_nonce, qty_nonce):
		self.book.add_bid(Order(self.book, price_ciphertext, qty_ciphertext, price_nonce, qty_nonce, "bid", self.next_id))
		self.next_id = self.next_id + 1
		
	def submit_ask(self, price_ciphertext, qty_ciphertext, price_nonce, qty_nonce):
		self.book.add_ask(Order(self.book, price_ciphertext, qty_ciphertext, price_nonce, qty_nonce, "ask", self.next_id))
		self.next_id = self.next_id + 1
		
	def get_history(self):
		s = ""
		for action in self.book.history:
			s += action + '\n'
		return s
