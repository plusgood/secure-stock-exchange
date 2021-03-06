import phe
from phe import paillier
import phe.util

class OrderBook:
	def __init__(self):
		self.bids = [] # ordered by increasing price
		self.asks = [] # ordered by decreasing price
		self.history = []
		self.public_key, self.private_key = paillier.generate_paillier_keypair()

	def decrypt(self, ciphertext):
		return self.private_key.raw_decrypt(ciphertext)

	def add_bid(self, bid):
		idx = self.find_bid(bid)
		self.bids.insert(idx, bid)
		self.history.append("Received order {0} (bid)".format(bid.id))
		self.match()

	def add_ask(self, ask):
		idx = self.find_ask(ask)
		self.asks.insert(idx, ask)
		self.history.append("Received order {0} (ask)".format(ask.id))
		self.match()

	'''
	Returns the index of the lowest-price bid amongst bids priced above the given one
	'''
	def find_bid(self, bid):
		lower = -1
		upper = len(self.bids)
		while upper - lower > 1:
			index = (lower + upper)//2
			if self.bids[index].price > bid.price:
				upper = index
			else:
				lower = index
		return upper

	'''
	Returns the index of the highest-price ask amongst asks priced below the given one
	'''
	def find_ask(self, ask):
		lower = -1
		upper = len(self.asks)
		while upper - lower > 1:
			index = (lower + upper)//2
			if self.asks[index].price < ask.price:
				upper = index
			else:
				lower = index
		return upper

	def match(self):
		while len(self.bids) > 0 and len(self.asks) > 0:
			best_bid = self.bids[-1]
			best_ask = self.asks[-1]
			if best_bid.price < best_ask.price:
				# best bid/ask don't match
				break
			matched_qty = min(best_bid.quantity, best_ask.quantity)
			self.history.append("Matched bid {0} with ask {1} for quantity {2}"
								.format(best_bid.id, best_ask.id, matched_qty))

			small, big = sorted([best_bid, best_ask], key=lambda x: (x.quantity, x.direction))
			i, j = small.id, big.id

			self.history.append('Proof for match: r_p_{j}/r_p_{i} = {0}, ' \
								'q_{j} - q_{i} - 1 = {1}, ' \
								'p_{j} - p_{i} = {2}'
								 .format(big.price_nonce * phe.util.invert(small.price_nonce, self.public_key.n**2),
										 big.quantity - small.quantity - 1,
										 big.price - small.price,
										 i=i, j=j))

			best_bid.quantity -= matched_qty
			best_ask.quantity -= matched_qty
			if best_bid.quantity == 0:
				self.bids.remove(best_bid)
				self.history.append("Bid {} filled, removed from orderbook. Price nonce: {}. Quantity nonce: {}."
									.format(best_bid.id, best_bid.price_nonce, best_bid.qty_nonce))
			if best_ask.quantity == 0:
				self.asks.remove(best_ask)
				self.history.append("Ask {} filled, removed from orderbook. Price nonce: {}. Quantity nonce: {}."
									.format(best_ask.id, best_ask.price_nonce, best_ask.qty_nonce))

	def get_unencrypted_book(self):
		s = "Bids:\n"
		for bid in self.bids:
			s += "ID: {0} Price: {1} Quantity: {2}\n".format(bid.id, bid.price, bid.quantity)
		s += "\nAsks:\n"
		for ask in self.asks:
			s += "ID: {0} Price: {1} Quantity: {2}\n".format(ask.id, ask.price, ask.quantity)
		return s

	def get_encrypted_book(self):
		s = "Bids:\n"
		for bid in self.bids:
			s += "ID: {0} Price: {1} Quantity: {2}\n".format(bid.id, bid.price_ciphertext, bid.qty_ciphertext)
		s += "\nAsks:\n"
		for ask in self.asks:
			s += "ID: {0} Price: {1} Quantity: {2}\n".format(ask.id, ask.price_ciphertext, ask.qty_ciphertext)
		return s

class Order:
	def __init__(self, book, price_ciphertext, qty_ciphertext, price_nonce, qty_nonce, direction, id):
		self.book = book
		self.price_ciphertext = price_ciphertext
		self.qty_ciphertext = qty_ciphertext
		self.price_nonce = price_nonce
		self.qty_nonce = qty_nonce
		self.direction = direction
		self.id = id
		assert direction in ['ask', 'bid']
		self.price = book.decrypt(price_ciphertext)
		self.quantity = book.decrypt(qty_ciphertext)
		assert self.price > 0
		assert self.quantity > 0
