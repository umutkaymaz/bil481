import tkinter as tk
from tkinter import ttk
#Tüm global değişkenleri barındırıyor.
sepet = {}

menu_data = {}

master :tk.Tk = None

sonucLabel : tk.Label = None
yemeksepeti_fiyatlarLabel :tk.Label = None
getir_fiyatlarLabel:tk.Label = None
migrosYemek_fiyatlarLabel:tk.Label = None

konum_girisi : tk.Entry = None 
restoran_girisi : tk.Entry = None
menu : ttk.Treeview = None
favorites_list : tk.Listbox = None

sepet_icerik : tk.StringVar = None
selected_food_var : tk.StringVar = None 

var_joker : tk.IntVar = None
var_tok: tk.IntVar = None 
var_flas: tk.IntVar = None 
miktar_var: tk.IntVar = None 
favorite_var: tk.IntVar = None 