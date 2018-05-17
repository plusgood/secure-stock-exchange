# Cryptographically secure exchange

In this repository we implement a cryptographically secure exchange based on homomorphic encryption -- specifically the Paillier cryptosystem -- as described in http://www.eecs.harvard.edu/~cat/cm.pdf.

To use this repository, run ``server.py``, which exposes a Flask server at ``localhost:5000``. From there either ``UI.py`` may be run to expose a ``tkinter`` interface, or ``client.py`` may be run to expose a text one. Manual solutions are also possible: the server accepts POST requests to ``localhost:5000/submit-order`` containing fields of encrypted price, encrypted quantity, price nonce, quantity nonce, and order type (bid or ask). The relevant part of the public key (i.e. n) may be obtained from ``localhost:5000/public-key``. 

The server also accepts GET requests to ``/order-book``, which displays a text version of the encrypted order book separated into bids and asks. The book is guaranteed to be ordered in increasing (for bids) and decreasing (for asks) order respectively, but does not expose any information about the prices and quantities otherwise. For debugging purposes GET requests to ``/raw-order-book`` are also accepted, which displays the decrypted order book. Also accepted are GET requests to ``/history``, which displays the entire history of the server's operation, including proofs of correctness upon matching orders and revealed nonces upon orders being entirely filled.

This implementation is developed as part of a project for MIT's 6.857 Computer and Network Security class. Our associated paper may eventually be found at http://courses.csail.mit.edu/6.857/2018/projects.

### Dependencies
  	
~~~~
pip3 install flask
pip3 install phe
~~~~
