import pytest
import tkinter as tk
from tkinter import ttk
from GUI_actions import guncelle_sepet

root = tk.Tcl()
pseudo_sepet_icerik = tk.StringVar(root)

@pytest.mark.parametrize("sepet, sepet_icerik,sonuc", [
    ({"kebap": 10}, pseudo_sepet_icerik,"kebap: 10\n"), #Yemeksepeti indirimsiz
    
])

def test_guncelle_sepet(sepet : dict, sepet_icerik : tk.StringVar,sonuc):
    guncelle_sepet(sepet, sepet_icerik)
    assert sepet_icerik.get() == sonuc


