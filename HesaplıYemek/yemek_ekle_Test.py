import pytest
import tkinter as tk
from tkinter import ttk
from GUI_actions import yemek_ekle
import config

root = tk.Tk()

config.menu = ttk.Treeview(root, columns=("Yemek",), show="headings")
config.menu.heading("Yemek", text="Yemek")
config.menu.pack()

config.yemeksepeti_fiyatlarLabel = tk.Label(root)
config.getir_fiyatlarLabel = tk.Label(root)
config.migrosYemek_fiyatlarLabel = tk.Label(root)

Yemeksepeti_J = tk.StringVar(root)
Getir_J = tk.StringVar(root)
Migros_J = tk.StringVar(root)
pseudo_sepet_icerik = tk.StringVar(root)
pseudo_food_var = tk.StringVar(root)
pseudo_miktar_var = tk.IntVar(root)

@pytest.mark.parametrize(
    "joker_yemeksepeti, joker_getir, joker_migros, sepet_icerik, selected_food_var, sepet, miktar_var, menu_data,dummy_yemek, sonuc",
    [
        (Yemeksepeti_J, Getir_J, Migros_J, pseudo_sepet_icerik, pseudo_food_var,
          {"Cheeseburger": 10}, pseudo_miktar_var, {"Cheeseburger": {"Yemeksepeti": 350, "Getir": 330, "MigrosYemek": 330}},"Cheeseburger", 11),
        
        (Yemeksepeti_J, Getir_J, Migros_J, pseudo_sepet_icerik, pseudo_food_var,
          {"a": 8}, pseudo_miktar_var, {"a": {"Yemeksepeti": 350, "Getir": 330, "MigrosYemek": 330}},"a", 9),
        
        (Yemeksepeti_J, Getir_J, Migros_J, pseudo_sepet_icerik, pseudo_food_var,
          {}, pseudo_miktar_var, {"a": {"Yemeksepeti": 350, "Getir": 330, "MigrosYemek": 330}},"a", 1),
    ]
)

def test_yemek_ekle(joker_yemeksepeti, joker_getir, joker_migros, sepet_icerik: tk.StringVar, selected_food_var: tk.StringVar,
                    sepet: dict, miktar_var: tk.IntVar, menu_data: dict,dummy_yemek, sonuc):
    selected_food_var.set(dummy_yemek)
    yemek_ekle(joker_yemeksepeti, joker_getir, joker_migros, sepet_icerik, selected_food_var,
                sepet, miktar_var, menu_data)
    assert miktar_var.get() == sonuc
