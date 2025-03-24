import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
from indirimhesabi import fiyatlari_hesapla
import GUI
##GUI daki değiskenleri aktardım

def guncelle_sepet(sepet : dict, sepet_icerik : tk.StringVar):
    
    """sepetteki ürünlerin guncel halini sepeti gösterdigimiz label'a aktarir."""
    
    text = ""
    
    for food, miktar in sepet.items():
        if miktar > 0:
            text += f"{food}: {miktar}\n"
    
    sepet_icerik.set(text)


def secilen_csv_guncelle(sepet : dict, menu_data: dict,sepet_icerik : tk.StringVar,
                         joker_yemeksepeti, joker_getir, joker_migros):
    
    """secilen.csv'yi günceller (sepet dict'ine göre)"""
    
    rows = []
    for food, miktar in sepet.items():
        
        if food in menu_data:
            data = menu_data[food]
            
            for x in range(miktar):
                rows.append(data)
    
    df = pd.DataFrame(rows, columns=["food", "Yemeksepeti", "Getir", "MigrosYemek"])
    df.to_csv("secilen.csv", index=False)
    guncelle_sepet(sepet,sepet_icerik)
    fiyatlari_hesapla(joker_yemeksepeti,joker_getir,joker_migros,sepet,menu_data)

##-----------yemek ekleme çıkarma---------------------
def yemek_ekle(joker_yemeksepeti, joker_getir, joker_migros,sepet_icerik :tk.StringVar,selected_food_var :tk.StringVar,
                sepet: dict, miktar_var : tk.IntVar, menu_data: dict):
    """
        sepette verilen türde 1 adet yemek ekle.
    """
    yemek = selected_food_var.get()
    #yemek secilmediyse bir sey yapma
    if not yemek:
        return
    else:
        sepet[yemek] = sepet.get(yemek, 0) + 1
        miktar_var.set(sepet[yemek])
        secilen_csv_guncelle(sepet, menu_data,sepet_icerik,joker_yemeksepeti, joker_getir, joker_migros)


def yemek_sil(joker_yemeksepeti, joker_getir, joker_migros,sepet_icerik :tk.StringVar,selected_food_var :tk.StringVar,
                sepet: dict, miktar_var : tk.IntVar, menu_data: dict):
    """
        sepetten verilen türde 1 adet yemek cıkar.
    """
    yemek = selected_food_var.get()
    if not yemek:
        return
    if sepet.get(yemek, 0) > 0:
        sepet[yemek] -= 1
    miktar_var.set(sepet.get(yemek, 0))
    secilen_csv_guncelle(sepet, menu_data,sepet_icerik,joker_yemeksepeti, joker_getir, joker_migros)


def yemek_sec(event, sepet : dict, selected_food_var : tk.StringVar, miktar_var: tk.IntVar):

    """Secilen yemegi, miktar kontrol alanina aktarma.""" 

    secili = GUI.menu.selection()
    if secili:
        food = GUI.menu.item(secili[0])["values"][0]
        selected_food_var.set(food)
        miktar_var.set(sepet.get(food, 0))

##-----------yemek ekleme çıkarma---------------------

#---------------favorilerle alakalı kısım-----------------

def favorileri_yaz():
    """ "favori.csv" dosyasindaki favorileri liste kutusuna yukleme."""
    GUI.favorites_list.delete(0, tk.END)
    try:
        df = pd.read_csv("favori.csv")
        for _, row in df.iterrows():
            fav_entry = f"{row['Konum']} - {row['Restoran']}"
            GUI.favorites_list.insert(tk.END, fav_entry)
    except FileNotFoundError:
        pass






def favori_guncelle():
    # Favori checkbox'un durumuna gore "favori.csv"'yi günceller.
    yer = GUI.konum_girisi.get().strip()
    lokanta = GUI.restoran_girisi.get().strip()
    if not yer or not lokanta:
        return
    try:
        df = pd.read_csv("favori.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Konum", "Restoran"])
    if GUI.favorite_var.get() == 1:  # Ekleme checkbox isaretli ise eklenmis ya da yeni ekleniyor olmalı
        if not (((df["Konum"] == yer) & (df["Restoran"] == lokanta)).any()): #yoksa ekle
            new_row = pd.DataFrame([[yer, lokanta]], columns=["Konum", "Restoran"])
            df = pd.concat([df, new_row], ignore_index=True)
    else:  # Kaldırma
        df = df[~((df["Konum"] == yer) & (df["Restoran"] == lokanta))] 
    df.to_csv("favori.csv", index=False)
    favorileri_yaz()

#---------------favorilerle alakalı kısım-----------------


def fiyatlari_getir(menu_data : dict,favorite_var : tk.IntVar):

    """ Fiyat getirme methodu. """

    yer = GUI.konum_girisi.get()
    lokanta = GUI.restoran_girisi.get()

    if not yer or not lokanta:
        GUI.sonucLabel.config(text="Lütfen adres ve restoran giriniz.")
        return
    
    try:
        df = pd.read_csv("menu.csv")
    except FileNotFoundError:
        GUI.sonucLabel.config(text="menu.csv bulunamadi!")
        return
    
    GUI.menu.delete(*GUI.menu.get_children())

    menu_data.clear()
    
    for _, row in df.iterrows():
        food = row["food"]
        prices = {"food": food, "Yemeksepeti": row["Yemeksepeti"], "Getir": row["Getir"], "MigrosYemek": row["MigrosYemek"]}
        menu_data[food] = prices
        GUI.menu.insert("", "end", values=(food, prices["Yemeksepeti"], prices["Getir"], prices["MigrosYemek"]))
    
    GUI.sonucLabel.config(text=f"{yer}, {lokanta} için sonuçlar")
    
    # "favori.csv"'de bu restoran varsa, checkboxun isaretli olmasi.
    
    try:
        favorite_df = pd.read_csv("favori.csv")
        if ((favorite_df["Konum"] == yer) & (favorite_df["Restoran"] == lokanta)).any():
            favorite_var.set(1)
        else:
            favorite_var.set(0)

    except FileNotFoundError:
        favorite_var.set(0)
    
    favorileri_yaz()


def favori_sec(event,menu_data:dict,favorite_var : tk.IntVar):
    """ Favoriler listesinde seçilen favoriyi alıp konumla restoran alanlarını otomatik doldurma. """
    secim = GUI.favorites_list.curselection()
    if secim:
        fav = GUI.favorites_list.get(secim[0])
        parts = fav.split(" - ")
        if len(parts) == 2:
            GUI.konum_girisi.delete(0, tk.END)
            GUI.konum_girisi.insert(0, parts[0])
            GUI.restoran_girisi.delete(0, tk.END)
            GUI.restoran_girisi.insert(0, parts[1])
            fiyatlari_getir(menu_data,favorite_var)
