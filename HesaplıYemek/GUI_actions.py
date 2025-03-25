import tkinter as tk
from tkinter import ttk
import pandas as pd
import config
from indirimhesabi import hesapla_indirim
##GUI daki değiskenleri aktardım
#Sadece GUI'daki compenentları frame label, Entry, Treeview,checkboxlar gibi yapıları parametre olarak değil global değişken olarak aktardım.

def fiyatlari_hesapla(joker_yemeksepeti, joker_getir, joker_migros, sepet : dict, menu_data : dict):
    
    """Sepetteki ürünlerin her site için toplam fiyati, indirim miktari ve indirimli fiyatini hesaplar.
        Parametreler:
        joker_yemeksepeti, joker_getir, joker_migros: ilgili platformda indirim varsa 1'e eşit aksi taktirde 0 değeri alir.
        sepet: {yemek adi : yemek miktari} şeklinde kullacinin oluşturduğu sepeti tutar
        menu_data: {"food": yemek adi, "Yemeksepeti": Yemeksepeti_fiyati , "Getir": Getir_fiyati, "MigrosYemek": MigrosYemek_fiyati}
        yemeksepeti_fiyatlarLabel, getir_fiyatlarLabel, migrosYemek_fiyatlarLabel:
             "Markalarin indirimsiz fiyatini , indirim miktarini ve indirimli fiyatini gösteren label'lar "

        Ardindan bu değerleri label'larin text'ine yazar.

        herhangi bir şey return etmez

    """
    
    toplam_yemeksepeti = 0
    toplam_getir = 0
    toplam_MigrosYemek = 0

    for food, miktar in sepet.items():
        if food in menu_data:
            prices = menu_data[food]
            toplam_yemeksepeti += prices["Yemeksepeti"] * miktar
            toplam_getir += prices["Getir"] * miktar
            toplam_MigrosYemek += prices["MigrosYemek"] * miktar

    toplam_fiyat_yemeksepeti, indirim_yemeksepeti, indirimli_yemeksepeti = hesapla_indirim(toplam_yemeksepeti, joker_yemeksepeti, 1)
    toplam_fiyat_getir, indirim_getir, indirimli_getir = hesapla_indirim(toplam_getir, joker_getir, 2)
    toplam_fiyat_migros, indirim_migros, indirimli_migros = hesapla_indirim(toplam_MigrosYemek, joker_migros, 3)

    config.yemeksepeti_fiyatlarLabel.config(foreground="purple",text=f"Yemeksepeti: Toplam {toplam_fiyat_yemeksepeti} TL, İndirim {indirim_yemeksepeti} TL, İndirimli {indirimli_yemeksepeti} TL")
    config.getir_fiyatlarLabel.config(foreground="purple",text=f"Getir: Toplam {toplam_fiyat_getir} TL, İndirim {indirim_getir} TL, İndirimli {indirimli_getir} TL")
    config.migrosYemek_fiyatlarLabel.config(foreground="purple",text=f"MigrosYemek: Toplam {toplam_fiyat_migros} TL, İndirim {indirim_migros} TL, İndirimli {indirimli_migros} TL")

    
    fiyatList = {indirimli_yemeksepeti : "yemeksepeti", indirimli_getir: "getir",indirimli_migros: "migros"}
    fiyatMin = float('inf') #sonsuz büyüklükte sayı atadım
    appMin = ""
    
    for fiyat,app in fiyatList.items():
        if(fiyatMin > fiyat):
            fiyatMin = fiyat
            appMin = app
    
    #en ucuzu kırmızı göster.
    match appMin:
        case "yemeksepeti":
            config.yemeksepeti_fiyatlarLabel.config(foreground="red")
        case "getir":
            config.getir_fiyatlarLabel.config(foreground="red")
        case "migros":
            config.migrosYemek_fiyatlarLabel.config(foreground="red")
        case  _:
            print(appMin)



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


def yemek_sec(sepet : dict, selected_food_var : tk.StringVar, miktar_var: tk.IntVar):

    """Secilen yemegi, miktar kontrol alanina aktarma.""" 

    secili = config.menu.selection()
    if secili:
        food = config.menu.item(secili[0])["values"][0]
        selected_food_var.set(food)
        miktar_var.set(sepet.get(food, 0))

##-----------yemek ekleme çıkarma---------------------

#---------------favorilerle alakalı kısım-----------------

def favorileri_yaz():
    """ "favori.csv" dosyasindaki favorileri liste kutusuna yukleme."""
    config.favorites_list.delete(0, tk.END)
    try:
        df = pd.read_csv("favori.csv")
        for _, row in df.iterrows():
            fav_entry = f"{row['Konum']} - {row['Restoran']}"
            config.favorites_list.insert(tk.END, fav_entry)
    except FileNotFoundError:
        pass






def favori_guncelle():
    # Favori checkbox'un durumuna gore "favori.csv"'yi günceller.
    yer = config.konum_girisi.get().strip()
    lokanta = config.restoran_girisi.get().strip()
    if not yer or not lokanta:
        return
    try:
        df = pd.read_csv("favori.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Konum", "Restoran"])
    if config.favorite_var.get() == 1:  # Ekleme checkbox isaretli ise eklenmis ya da yeni ekleniyor olmalı
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

    yer = config.konum_girisi.get()
    lokanta = config.restoran_girisi.get()

    if not yer or not lokanta:
        config.sonucLabel.config(text="Lütfen adres ve restoran giriniz.")
        return
    
    try:
        df = pd.read_csv("menu.csv")
    except FileNotFoundError:
        config.sonucLabel.config(text="menu.csv bulunamadi!")
        return
    
    config.menu.delete(*config.menu.get_children())

    menu_data.clear()
    
    for _, row in df.iterrows():
        food = row["food"]
        prices = {"food": food, "Yemeksepeti": row["Yemeksepeti"], "Getir": row["Getir"], "MigrosYemek": row["MigrosYemek"]}
        menu_data[food] = prices
        config.menu.insert("", "end", values=(food, prices["Yemeksepeti"], prices["Getir"], prices["MigrosYemek"]))
    
    config.sonucLabel.config(text=f"{yer}, {lokanta} için sonuçlar")
    
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


def favori_sec(menu_data:dict,favorite_var : tk.IntVar):
    """ Favoriler listesinde seçilen favoriyi alıp konumla restoran alanlarını otomatik doldurma. """
    secim = config.favorites_list.curselection()
    if secim:
        fav = config.favorites_list.get(secim[0])
        parts = fav.split(" - ")
        if len(parts) == 2:
            config.konum_girisi.delete(0, tk.END)
            config.konum_girisi.insert(0, parts[0])
            config.restoran_girisi.delete(0, tk.END)
            config.restoran_girisi.insert(0, parts[1])
            fiyatlari_getir(menu_data,favorite_var)
