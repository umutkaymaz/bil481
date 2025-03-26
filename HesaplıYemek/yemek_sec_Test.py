import pytest
import tkinter as tk
from tkinter import ttk
from GUI_actions import yemek_sec
import config

root = tk.Tk()

# Creates and configures the menu widget in config for yemek_sec.
# Essantial for avoiding "AttributeError"
config.menu = ttk.Treeview(root, columns=("Yemek",), show="headings")
config.menu.heading("Yemek", text="Yemek")
config.menu.pack()

pseudo_sepet = "Cheeseburger"
pseudo_amount = 10
# These two should be changed for testing different type and amount of foods.

item_id = config.menu.insert("", "end", values=(pseudo_sepet,))
config.menu.selection_set(item_id)

pseudo_food_var = tk.StringVar(root)
pseudo_miktar_var = tk.IntVar(root)

@pytest.mark.parametrize("sepet, selected_food_var, miktar_var, sonuc1, sonuc2", [
    ({pseudo_sepet: pseudo_amount}, pseudo_food_var, pseudo_miktar_var, pseudo_sepet, pseudo_amount),
])
def test_yemek_sec(sepet: dict, selected_food_var: tk.StringVar, miktar_var: tk.IntVar, sonuc1, sonuc2):
    
    yemek_sec(sepet, selected_food_var, miktar_var)
    assert selected_food_var.get() == sonuc1
    assert miktar_var.get() == sonuc2
