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

@given("Uygulama başlatılmıştır")
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
    config.yemeksepeti_fiyatlarLabel = ttk.Label(config.master, text="")
    config.getir_fiyatlarLabel =  ttk.Label(config.master, text="")
    config.migrosYemek_fiyatlarLabel =  ttk.Label(config.master, text="")

    GUI_actions.fiyatlari_getir(config.menu_data,config.favorite_var)
    print("Uygulama başlatıldı.")

@given('Menüde "{yemek}" adlı bir yemek listelenmektedir')
def step_impl(context, yemek):
    logger.info(f"Menu listing for '{yemek}'.")
    print(f"Menüde {yemek} listelendi.")

@when('Kullanıcı "{yemek}" yemeğini seçer')
def step_impl(context, yemek):
    config.selected_food_var.set("Pizza")
    GUI_actions.yemek_sec(config.sepet, config.selected_food_var, config.miktar_var)
    logger.info(f"User selected food '{yemek}'.")
    print(f"Kullanıcı {yemek} yemeğini seçti.")

@when("Kullanıcı \"+\" butonuna tıklar")
def step_impl(context):
    logger.info("User clicked '+' button.")
    print("Kullanıcı '+' butonuna tıkladı.")
    GUI_actions.yemek_ekle(config.var_joker, config.var_tok, config.var_flas,config.sepet_icerik,config.selected_food_var,
                config.sepet, config.miktar_var, config.menu_data)
    

@then('Sepet etiketinde "{expected_text}" görünmelidir')
def step_impl(context, expected_text):
    actual_text = config.sepet_icerik.get()
    if expected_text in actual_text:
        logger.info(f"PASS: Cart label contains expected text '{expected_text}'.")
    else:
        logger.error(f"FAIL: Cart label does not contain expected text '{expected_text}'. Actual text: '{actual_text}'.")
    assert expected_text in actual_text, f"Expected: {expected_text}, Obtained: {actual_text}"
    print("Sepet etiketi dogrulandi.")