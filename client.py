import requests
import phe
import random
from phe import paillier
from phe import PaillierPublicKey

URL = "http://127.0.0.1:5000"
public_key_n = int(requests.get(URL + "/public-key").text)
public_key = PaillierPublicKey(public_key_n)

def submit_order(price, quantity, direction):
	price_nonce = random.randint(0, 1 << 32)
	encrypted_price = int(public_key.encrypt(price, r_value=price_nonce).ciphertext())
	qty_nonce = random.randint(0, 1 << 32)
	encrypted_qty = int(public_key.encrypt(quantity, r_value=qty_nonce).ciphertext())
	data = {"encrypted_price": encrypted_price, "encrypted_qty": encrypted_qty, "price_nonce": price_nonce, "qty_nonce": qty_nonce, "direction": direction}
	r = requests.post(URL + "/submit-order", data)
	
if __name__ == "__main__":
	while True:
		price = int(input("Price?"))
		qty = int(input("Quantity?"))
		direction = str(input("Direction?"))
		submit_order(price, qty, direction)


