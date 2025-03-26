from behave import given, when, then
import sys
sys.path.append("C:/Users/LENOVO/Desktop/481Deneme")
import config
import GUI_actions
import tkinter as tk
from tkinter import ttk

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
    print(f"Menüde {yemek} listelendi.")

@when('Kullanıcı "{yemek}" yemeğini seçer')
def step_impl(context, yemek):
    config.selected_food_var.set("Pizza")
    GUI_actions.yemek_sec(config.sepet, config.selected_food_var, config.miktar_var)
    print(f"Kullanıcı {yemek} yemeğini seçti.")

@when("Kullanıcı \"+\" butonuna tıklar")
def step_impl(context):
    print("Kullanıcı '+' butonuna tıkladı.")
    GUI_actions.yemek_ekle(config.var_joker, config.var_tok, config.var_flas,config.sepet_icerik,config.selected_food_var,
                config.sepet, config.miktar_var, config.menu_data)
    

@then('Sepet etiketinde "{expected_text}" görünmelidir')
def step_impl(context, expected_text):
    actual_text = config.sepet_icerik.get()
    assert expected_text in actual_text, f"Beklenen: {expected_text}, Alınan: {actual_text}"
    print("Sepet etiketi doğrulandı.")