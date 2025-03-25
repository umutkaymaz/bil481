import pytest
import tkinter as tk
from tkinter import ttk
from GUI_actions import favori_guncelle
from GUI_actions import favorileri_yaz

root = tk.Tcl()
pseudo_sepet_icerik = tk.StringVar(root)

@pytest.mark.parametrize("sepet, sepet_icerik,sonuc", [
    ({"kebap": 10}, pseudo_sepet_icerik,"kebap: 10\n"),
    ({"kebap": 10,"a" : 54}, pseudo_sepet_icerik,"kebap: 10\na: 54\n"),
    ({"z" : 32,"x" : 61,"y" : 0,"muz" : 2}, pseudo_sepet_icerik,"z: 32\nx: 61\nmuz: 2\n"),
    ({"z" : 32,"x" : 61,"y" : 4,"muz" : 2}, pseudo_sepet_icerik,"z: 32\nx: 61\ny: 4\nmuz: 2\n"),
    
    ({"pizza": 3}, pseudo_sepet_icerik,"pizza: 3\n"),
    ({"pizza": 2,"tantuni" : 3}, pseudo_sepet_icerik,"pizza: 2\ntantuni: 3\n"),
    ({"doner" : 2,"x" : -12,"y" : 0,"muz" : 2}, pseudo_sepet_icerik,"doner: 2\nmuz: 2\n"),
    ({"doner" : 1,"x" : 6,"muz" : 2}, pseudo_sepet_icerik,"doner: 1\nx: 6\nmuz: 2\n")
    
])

def test_favoriler(sepet : dict, sepet_icerik : tk.StringVar,sonuc):
    (sepet, sepet_icerik)
    assert sepet_icerik.get() == sonuc

