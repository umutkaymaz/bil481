import pytest
import tkinter as tk
from tkinter import ttk
from GUI_actions import yemek_sec
import config
import logging

logger = logging.getLogger("testLogger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("test.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

root = tk.Tk()

# Creates and configures the menu widget in config for yemek_sec.
config.menu = ttk.Treeview(root, columns=("Yemek",), show="headings")
config.menu.heading("Yemek", text="Yemek")
config.menu.pack()




pseudo_food_var = tk.StringVar(root)
pseudo_miktar_var = tk.IntVar(root)

@pytest.mark.parametrize("sepet, selected_food_var, miktar_var,yemek_adı, sonuc1, sonuc2", [
    ({"Cheeseburger": 10}, pseudo_food_var, pseudo_miktar_var,"Cheeseburger","Cheeseburger", 10),
    ({"Pizza": 5}, pseudo_food_var, pseudo_miktar_var,"Pizza", "Pizza", 5),
    ({"Doner": 3}, pseudo_food_var, pseudo_miktar_var, "Doner","Doner", 3),
    ({"Lahmacun": 7}, pseudo_food_var, pseudo_miktar_var, "Lahmacun", "Lahmacun", 7),
    ({"Burger": 2}, pseudo_food_var, pseudo_miktar_var, "Burger", "Burger", 2),
    ({"Kebap": 4}, pseudo_food_var, pseudo_miktar_var, "Kebap", "Kebap", 4),
    ({"Sushi": 8}, pseudo_food_var, pseudo_miktar_var, "Sushi", "Sushi", 8),
    ({"Taco": 6}, pseudo_food_var, pseudo_miktar_var, "Taco", "Taco", 6),
    ({"Salad": 1}, pseudo_food_var, pseudo_miktar_var, "Salad", "Salad", 1)
])
def test_yemek_sec(sepet: dict, selected_food_var: tk.StringVar, miktar_var: tk.IntVar, yemek_adı,sonuc1, sonuc2):
    
    pseudo_sepet = yemek_adı
    item_id = config.menu.insert("", "end", values=(pseudo_sepet))
    config.menu.selection_set(item_id)
    yemek_sec(sepet, selected_food_var, miktar_var)
    obtained_food = selected_food_var.get()
    obtained_amount = miktar_var.get()
    
    if obtained_food == sonuc1 and obtained_amount == sonuc2:
        logger.info(f"PASS: Food selection test for '{obtained_food}': expected ({sonuc1}, {sonuc2}), obtained ({obtained_food}, {obtained_amount})")
    else:
        logger.error(f"FAIL: Food selection test for '{obtained_food}': expected ({sonuc1}, {sonuc2}), obtained ({obtained_food}, {obtained_amount})")
    
    assert obtained_food == sonuc1
    assert obtained_amount == sonuc2
