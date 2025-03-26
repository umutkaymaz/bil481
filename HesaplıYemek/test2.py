import pytest
import tkinter as tk
from tkinter import ttk
from GUI_actions import fiyatlari_getir
import config

root = tk.Tcl()
pseudo_sepet_icerik = tk.StringVar(root)
a = tk.StringVar(root)
config.konum_girisi = tk.Entry(root,textvariable=a)
config.restoran_girisi = tk.Entry(root,textvariable=a)
config.sonucLabel = tk.Label(root)
config.menu = ttk.Treeview(root, columns=("Yemek", "YemekSepeti", "Getir", "MigrosYemek"), show="headings")
config.menu_data = {}

@pytest.mark.parametrize("menu_data, favorite_var, sonuc", [
    (config.menu_data, 0,"" ),
])

def fiyatlari_getir_test(menu_data : dict,favorite_var : tk.IntVar,sonuc):
    fiyatlari_getir(config.menu_data,config.favorite_var)
    for x in config.menu.get_children():
        assert config.menu.item(x)["values"] == ("Tavuk Burger",300,300,320)
        break

