from behave import given, when, then
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
import config
import GUI_actions
import tkinter as tk
from tkinter import ttk
import logging

logger = logging.getLogger("testLogger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("test.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

@given("Uygulama başladı")
def step_impl(context):
    context = config.master
    config.konum_girisi = ttk.Entry(config.master,textvariable="x")
    config.restoran_girisi = ttk.Entry(config.master,textvariable="x")
    config.sonucLabel = ttk.Label(config.master, text="")
    config.menu = ttk.Treeview(config.master, columns=("Yemek", "YemekSepeti", "Getir", "MigrosYemek"), show="headings")
    config.sepet_icerik = tk.StringVar()
    config.selected_food_var = tk.StringVar()
    config.var_joker  = tk.IntVar()
    config.var_tok= tk.IntVar() 
    config.var_flas = tk.IntVar() 
    config.miktar_var = tk.IntVar()  
    config.favorite_var = tk.IntVar()
    config.favorite_var.set(1)
    config.yemeksepeti_fiyatlarLabel = ttk.Label(config.master, text="")
    config.getir_fiyatlarLabel =  ttk.Label(config.master, text="")
    config.migrosYemek_fiyatlarLabel =  ttk.Label(config.master, text="")
    config.favorites_list = tk.Listbox(config.master)

    GUI_actions.fiyatlari_getir(config.menu_data,config.favorite_var)
    print("Uygulama başlatıldı.")

@given('Kullanıcı "{kullanici_konumu}" seklinde konumunu girmistir')
def step_impl(context, kullanici_konumu):
    config.restoran_girisi.insert(0,kullanici_konumu)
    logger.info(f"Kullanıcı konumunu girdi: {kullanici_konumu}")
    print("konum girildi")

@given('Kullanıcı "{lokanta}" isminde restoran bilgisini girer')
def step_impl(context, lokanta):
    config.restoran_girisi.insert(0,lokanta)
    logger.info(f"Kullanıcı restoran bilgisini girdi: {lokanta}")
    print("restoran girildi")

@when("Kullanıcı favori butonuna tıklar")
def step_impl(context):
    GUI_actions.favori_guncelle()
    logger.info("Kullanıcı favori butonuna tıkladı.")
    print("Kullanıcı favori butonuna tıkladı.")
    

@then('Favori listesinde  "{expected_text}" görünmelidir')
def step_impl(context, expected_text):
    actual_text = ""
    
    for x in config.favorites_list.get(0, "end"):
        actual_text += x
    
    if expected_text in actual_text:
        logger.info(f"PASS: Favori listesinde '{expected_text}' bulundu.")
    else:
        logger.error(f"FAIL: Favori listesinde '{expected_text}' bulunamadı. Alınan: '{actual_text}'")

    assert expected_text in actual_text, f"Beklenen: {expected_text}, Alınan: {actual_text}"
    print("Favori listesi doğrulandı.")