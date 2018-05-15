import phe
from order_book import OrderBook

class MarketOperator:

    def __init__(self):
        self.book = OrderBook()
        self.bulletin = ''

    def get_encrypted_book(self):
        return ''

