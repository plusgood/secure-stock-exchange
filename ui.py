from tkinter import *
from tkinter import messagebox
from tkinter.ttk import * 

window = Tk()
 
window.title("Cryptographic Securities Exchange")
 
window.geometry('400x200')

quantity_label = Label(window, text="Quantity")
price_label = Label(window, text="Price")
side_label = Label(window, text="Side")

quantity_label.grid(column=0, row=0)
price_label.grid(column=0, row=1)
side_label.grid(column=0, row=2)
 
quantity_box = Entry(window,width=10)
quantity_box.grid(column=1, row=0)

price_box = Entry(window,width=10)
price_box.grid(column=1, row=1)

side_dropdown = Combobox(window, text="Side", width=7, state='readonly')
side_dropdown['values']= ("Bid", "Ask")
side_dropdown.grid(column=1, row=2)
 
def clicked():
	qty = quantity_box.get()
	price = price_box.get()
	side = side_dropdown.get()
	messagebox.showinfo("Order Receipt", "Quantity: " + qty + "\n" + "Price: " + price + "\n" + "Side: " + side)
 
btn = Button(window, text="Send Order", command=clicked)
btn.grid(column=2, row=2)
 
window.mainloop()