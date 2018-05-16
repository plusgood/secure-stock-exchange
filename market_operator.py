import phe
from order_book import OrderBook
from order_book import Order

class MarketOperator:

	def __init__(self):
		self.book = OrderBook()
		self.next_id = 0
		self.bulletin = ''

	def get_encrypted_book(self):
		return self.book.get_unencrypted_book()
		
	def submit_bid(self, price, quantity):
		self.book.add_bid(Order(price, quantity, "bid", self.next_id))
		self.next_id = self.next_id + 1
		
	def submit_ask(self, price, quantity):
		self.book.add_ask(Order(price, quantity, "ask", self.next_id))
		self.next_id = self.next_id + 1
		
	def get_history(self):
		s = ""
		for action in self.book.history:
			s += action + '\n'
		return s
