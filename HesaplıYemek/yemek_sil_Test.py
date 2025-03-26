import pytest
import tkinter as tk
from tkinter import ttk
from GUI_actions import yemek_sil
import config
import logging

logger = logging.getLogger("testLogger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("test.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

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
    "joker_yemeksepeti, joker_getir, joker_migros, sepet_icerik, selected_food_var, sepet, miktar_var, menu_data, sonuc",
    [
        (
            Yemeksepeti_J, Getir_J, Migros_J, pseudo_sepet_icerik, pseudo_food_var,
            {"Cheeseburger": 10}, pseudo_miktar_var,
            {"Cheeseburger": {"Yemeksepeti": 350, "Getir": 330, "MigrosYemek": 330}}, 9
        )
    ]
)
def test_yemek_sil(joker_yemeksepeti, joker_getir, joker_migros, sepet_icerik, selected_food_var: tk.StringVar,
                   sepet: dict, miktar_var: tk.IntVar, menu_data: dict, sonuc):
    selected_food_var.set("Cheeseburger")
    yemek_sil(joker_yemeksepeti, joker_getir, joker_migros, sepet_icerik, selected_food_var, sepet, miktar_var, menu_data)
    obtained = miktar_var.get()
    food_name = selected_food_var.get()
    if obtained == sonuc:
        logger.info(f"PASS: Food removal test for '{food_name}': expected {sonuc}, obtained {obtained}")
    else:
        logger.error(f"FAIL: Food removal test for '{food_name}': expected {sonuc}, obtained {obtained}")
    assert obtained == sonuc
