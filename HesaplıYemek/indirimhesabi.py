import tkinter as tk
from tkinter import ttk
import GUI
def hesapla_indirim(toplam_fiyat, joker, site):
    """
    Verilen toplam fiyata göre indirim miktarini ve 
    indirimli fiyati hesaplar.
    
    joker == 1 ise indirim var 

    site == 1 ise Yemeksepeti
    site == 2 ise getir
    site == 3 ise MigrosYemek

    (toplam_fiyat, indirim_miktari, indirimli_fiyat) şeklimnde tuple döndürür.
    
    """
    indirim_miktari = 0
    
    if(site==1 and joker==1):
        if(150<=toplam_fiyat<300):
            
            indirim_miktari=60
        elif(300<=toplam_fiyat<450):
        
            indirim_miktari=100
        elif(450<=toplam_fiyat):
        
            indirim_miktari=150
        else:
            indirim_miktari=0
    
    elif(site==2 and joker==1):
        if(200<=toplam_fiyat<300):
        
            indirim_miktari=75
        elif(300<=toplam_fiyat<450):
        
            indirim_miktari=100
        elif(450<=toplam_fiyat):
        
            indirim_miktari=150
        else:
            indirim_miktari=0
    
    elif(site==3 and joker==1):
        if(150<=toplam_fiyat<250):
            indirim_miktari=60
    
        elif(250<=toplam_fiyat<350):
            indirim_miktari = 90
    
        elif(350<=toplam_fiyat<450):
            indirim_miktari=120
    
        elif(450<=toplam_fiyat):
            indirim_miktari=150
    
        else:
            indirim_miktari=0
    
    else:
        indirim_miktari=0
      
    indirimli_fiyat = toplam_fiyat - indirim_miktari
    
    return toplam_fiyat, indirim_miktari, indirimli_fiyat


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

    GUI.yemeksepeti_fiyatlarLabel.config(foreground="purple",text=f"Yemeksepeti: Toplam {toplam_fiyat_yemeksepeti} TL, İndirim {indirim_yemeksepeti} TL, İndirimli {indirimli_yemeksepeti} TL")
    GUI.getir_fiyatlarLabel.config(foreground="purple",text=f"Getir: Toplam {toplam_fiyat_getir} TL, İndirim {indirim_getir} TL, İndirimli {indirimli_getir} TL")
    GUI.migrosYemek_fiyatlarLabel.config(foreground="purple",text=f"MigrosYemek: Toplam {toplam_fiyat_migros} TL, İndirim {indirim_migros} TL, İndirimli {indirimli_migros} TL")

    
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
            GUI.yemeksepeti_fiyatlarLabel.config(foreground="red")
        case "getir":
            GUI.getir_fiyatlarLabel.config(foreground="red")
        case "migros":
            GUI.migrosYemek_fiyatlarLabel.config(foreground="red")
        case  _:
            print(appMin)
