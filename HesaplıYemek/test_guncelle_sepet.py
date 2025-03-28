import pytest
import tkinter as tk
from tkinter import ttk
from GUI_actions import guncelle_sepet
import logging

# Special logger creation
logger = logging.getLogger("testLogger")
logger.setLevel(logging.DEBUG)

# Adding FileHandler
fh = logging.FileHandler("test.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

root = tk.Tcl()
pseudo_sepet_icerik = tk.StringVar(root)

@pytest.mark.parametrize("sepet, sepet_icerik, sonuc", [
    ({"kebap": 10}, pseudo_sepet_icerik, "kebap: 10\n"),
    ({"kebap": 10, "a": 54}, pseudo_sepet_icerik, "kebap: 10\na: 54\n"),
    ({"z": 32, "x": 61, "y": 0, "muz": 2}, pseudo_sepet_icerik, "z: 32\nx: 61\nmuz: 2\n"),
    ({"z": 32, "x": 61, "y": 4, "muz": 2}, pseudo_sepet_icerik, "z: 32\nx: 61\ny: 4\nmuz: 2\n"),
    ({"pizza": 3}, pseudo_sepet_icerik, "pizza: 3\n"),
    ({"pizza": 2, "tantuni": 3}, pseudo_sepet_icerik, "pizza: 2\ntantuni: 3\n"),
    ({"doner": 2, "x": -12, "y": 0, "muz": 2}, pseudo_sepet_icerik, "doner: 2\nmuz: 2\n"),
    ({"doner": 1, "x": 6, "muz": 2}, pseudo_sepet_icerik, "doner: 1\nx: 6\nmuz: 2\n")
])
def test_guncelle_sepet(sepet: dict, sepet_icerik: tk.StringVar, sonuc):
    guncelle_sepet(sepet, sepet_icerik)
    updated_content = sepet_icerik.get()
    if updated_content == sonuc:
        logger.info(f"PASS: Cart {sepet} expected output {sonuc} matches obtained output {updated_content}")
    else:
        logger.error(f"FAIL: Cart {sepet} expected output {sonuc} does not match obtained output {updated_content}")
    assert updated_content == sonuc
