import pytest
import tkinter as tk
from tkinter import ttk
from GUI_actions import yemek_ekle
import config
import logging

root = tk.Tk()

logger = logging.getLogger("testLogger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("test.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

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
    "joker_yemeksepeti, joker_getir, joker_migros, sepet_icerik, selected_food_var, sepet, miktar_var, menu_data, dummy_yemek, sonuc",
    [
        (Yemeksepeti_J, Getir_J, Migros_J, pseudo_sepet_icerik, pseudo_food_var,
          {"Cheeseburger": 10}, pseudo_miktar_var, {"Cheeseburger": {"Yemeksepeti": 350, "Getir": 330, "MigrosYemek": 330}}, "Cheeseburger", 11),
        
        (Yemeksepeti_J, Getir_J, Migros_J, pseudo_sepet_icerik, pseudo_food_var,
          {"a": 8}, pseudo_miktar_var, {"a": {"Yemeksepeti": 350, "Getir": 330, "MigrosYemek": 330}}, "a", 9),
        
        (Yemeksepeti_J, Getir_J, Migros_J, pseudo_sepet_icerik, pseudo_food_var,
          {}, pseudo_miktar_var, {"a": {"Yemeksepeti": 350, "Getir": 330, "MigrosYemek": 330}}, "a", 1),
    ]
)
def test_yemek_ekle(joker_yemeksepeti, joker_getir, joker_migros, sepet_icerik: tk.StringVar, selected_food_var: tk.StringVar,
                    sepet: dict, miktar_var: tk.IntVar, menu_data: dict, dummy_yemek, sonuc):
    selected_food_var.set(dummy_yemek)
    yemek_ekle(joker_yemeksepeti, joker_getir, joker_migros, sepet_icerik, selected_food_var,
                sepet, miktar_var, menu_data)

    obtained_miktar = miktar_var.get()
    
    if obtained_miktar == sonuc:
        logger.info(f"PASS: yemek_ekle test for '{dummy_yemek}': expected {sonuc}, obtained {obtained_miktar}")
    else:
        logger.error(f"FAIL: yemek_ekle test for '{dummy_yemek}': expected {sonuc}, obtained {obtained_miktar}")

    assert obtained_miktar == sonuc
