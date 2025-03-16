import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import indirimhesabi  
 
#sepeti bir dictionary de tutuyoruz.
sepet = {}

menu_data = {}   

indirim_yemeksepeti = 0.0
indirim_getir = 0.0
indirim_migrosYemek = 0.0

def secilen_csv_guncelle():
    """secilen.csv'yi günceller"""
    
    rows = []
    for food, miktar in sepet.items():
        
        if food in menu_data:
            data = menu_data[food]
            
            for x in range(miktar):
                rows.append(data)
    
    df = pd.DataFrame(rows, columns=["food", "Yemeksepeti", "Getir", "MigrosYemek"])
    df.to_csv("secilen.csv", index=False)
    guncelle_sepet()

def guncelle_sepet():
    
    """secilen.csv yi guide günceller."""
    
    text = "\n".join([f"{food}: {miktar}" for food, miktar in sepet.items() if miktar > 0])
    sepet_icerik.set(text)
    fiyatlari_hesapla()

def fiyatlari_hesapla():
    
    """Sepetteki ürünlerin her site için toplam fiyati, indirim miktari ve indirimli fiyatini hesaplar."""
    
    global indirim_yemeksepeti, indirim_getir, indirim_migrosYemek
    total_yemeksepeti = 0
    total_getir = 0
    total_MigrosYemek = 0
    for food, miktar in sepet.items():
        if food in menu_data:
            prices = menu_data[food]
            total_yemeksepeti += prices["Yemeksepeti"] * miktar
            total_getir += prices["Getir"] * miktar
            total_MigrosYemek += prices["MigrosYemek"] * miktar

    t_yemek, disc_yemek, discounted_yemek = indirimhesabi.hesapla_indirim(total_yemeksepeti, indirim_yemeksepeti, 1)
    t_getir, disc_getir, discounted_getir = indirimhesabi.hesapla_indirim(total_getir, indirim_getir, 2)
    t_MigrosYemek, disc_MigrosYemek, discounted_MigrosYemek = indirimhesabi.hesapla_indirim(total_MigrosYemek, indirim_migrosYemek, 3)

    yemeksepeti_fiyatlarLabel.config(text=f"Yemeksepeti: Toplam {t_yemek} TL, İndirim {disc_yemek} TL, İndirimli {discounted_yemek} TL")
    getir_fiyatlarLabel.config(text=f"Getir: Toplam {t_getir} TL, İndirim {disc_getir} TL, İndirimli {discounted_getir} TL")
    migrosYemek_fiyatlarLabel.config(text=f"MigrosYemek: Toplam {t_MigrosYemek} TL, İndirim {disc_MigrosYemek} TL, İndirimli {discounted_MigrosYemek} TL")

def fiyatlari_getir():

    """ Fiyat getirme methodu. """

    global menu_data
    yer = konum_girisi.get()
    lokanta = restoran_girisi.get()

    if not yer or not lokanta:
        sonucLabel.config(text="Lütfen adres ve restoran giriniz.")
        return
    
    try:
        df = pd.read_csv("menu.csv")
    except FileNotFoundError:
        sonucLabel.config(text="menu.csv bulunamadi!")
        return
    
    menu.delete(*menu.get_children())

    menu_data = {}
    
    for _, row in df.iterrows():
        food = row["food"]
        prices = {"food": food, "Yemeksepeti": row["Yemeksepeti"], "Getir": row["Getir"], "MigrosYemek": row["MigrosYemek"]}
        menu_data[food] = prices
        menu.insert("", "end", values=(food, prices["Yemeksepeti"], prices["Getir"], prices["MigrosYemek"]))
    
    sonucLabel.config(text=f"{yer}, {lokanta} için sonuçlar")
    
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

def yemek_sec(event):

    # Secilen yemegi, miktar kontrol alanina aktarma.

    secili = menu.selection()
    if secili:
        food = menu.item(secili[0])["values"][0]
        selected_food_var.set(food)
        miktar_var.set(sepet.get(food, 0))

def yemek_ekle():
    yemek = selected_food_var.get()
    if not yemek:
        return
    sepet[yemek] = sepet.get(yemek, 0) + 1
    miktar_var.set(sepet[yemek])
    secilen_csv_guncelle()

def yemek_sil():
    yemek = selected_food_var.get()
    if not yemek:
        return
    if sepet.get(yemek, 0) > 0:
        sepet[yemek] -= 1
    miktar_var.set(sepet.get(yemek, 0))
    secilen_csv_guncelle()

def indirim_guncelle():
    global indirim_yemeksepeti, indirim_getir, indirim_migrosYemek
    # Indirim kontrolu
    if var_joker.get() == 1:
        indirim_yemeksepeti = 1
    else:
        indirim_yemeksepeti = 0

    if var_tok.get() == 1:
        indirim_getir = 1
    else:
        indirim_getir = 0

    if var_flas.get() == 1:
        indirim_migrosYemek = 1
    else:
        indirim_migrosYemek = 0    
    fiyatlari_hesapla()

def favori_guncelle():
    # Favori checkbox'un durumuna gore "favori.csv"'yi günceller.
    yer = konum_girisi.get().strip()
    lokanta = restoran_girisi.get().strip()
    if not yer or not lokanta:
        return
    try:
        df = pd.read_csv("favori.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Konum", "Restoran"])
    if favorite_var.get() == 1:  # Ekleme
        if not (((df["Konum"] == yer) & (df["Restoran"] == lokanta)).any()):
            new_row = pd.DataFrame([[yer, lokanta]], columns=["Konum", "Restoran"])
            df = pd.concat([df, new_row], ignore_index=True)
    else:  # Kaldırma
        df = df[~((df["Konum"] == yer) & (df["Restoran"] == lokanta))] 
    df.to_csv("favori.csv", index=False)
    favorileri_yaz()

def favorileri_yaz():
    # "favori.csv" dosyasindaki favorileri liste kutusuna yukleme.
    favorites_list.delete(0, tk.END)
    try:
        df = pd.read_csv("favori.csv")
        for _, row in df.iterrows():
            fav_entry = f"{row['Konum']} - {row['Restoran']}"
            favorites_list.insert(tk.END, fav_entry)
    except FileNotFoundError:
        pass

def favori_sec(event):
    # Favoriler listesinde seçilen favoriyi alıp konumla restoran alanlarını otomatik dolurma.
    secim = favorites_list.curselection()
    if secim:
        fav = favorites_list.get(secim[0])
        parts = fav.split(" - ")
        if len(parts) == 2:
            konum_girisi.delete(0, tk.END)
            konum_girisi.insert(0, parts[0])
            restoran_girisi.delete(0, tk.END)
            restoran_girisi.insert(0, parts[1])
            fiyatlari_getir()

def run_gui():
    global sonucLabel, konum_girisi, restoran_girisi, menu, sepet_icerik, master
    global yemeksepeti_fiyatlarLabel, getir_fiyatlarLabel, migrosYemek_fiyatlarLabel
    global var_joker, var_tok, var_flas, selected_food_var, miktar_var, favorite_var, favorites_list

    master = tk.Tk()
    master.title("HesapliYemek")
    master.geometry("1200x800")

    main_frame = ttk.Frame(master,padding=30)
    main_frame.pack(fill=tk.BOTH, expand=True)#Main frame tüm siteyi kaplasın

    #-----------------Sol üst: input frame olacak, restoran ve konum girdileri alınacak----------------------
    
    input_frame = ttk.Frame(main_frame,padding=10)
    input_frame.grid(row=0, column=0, sticky="nw")

    #adres yazısı
    adresLabel = ttk.Label(input_frame, text="Adres:")
    adresLabel.grid(row=0, column=0, sticky="W")
    
    #adresin girildiği bölge
    konum_girisi = ttk.Entry(input_frame)
    konum_girisi.grid(row=0, column=1)
    
    #restoran yazısı
    RestoranLabel = ttk.Label(input_frame, text="Restoran:")
    RestoranLabel.grid(row=1, column=0, sticky="W")

    #restoran girildiği bölge
    restoran_girisi = ttk.Entry(input_frame)
    restoran_girisi.grid(row=1, column=1)
    
    #favorite_var = 1 ise chechkbox isaretli degil ise isaretsiz
    favorite_var = tk.IntVar()
    
    #toogle_favorite() çağır
    favori_checkbox = ttk.Checkbutton(input_frame, text="Favori", variable=favorite_var, command=favori_guncelle)
    favori_checkbox.grid(row=1, column=2)

    #fiyatlari_getir() çağır
    fiyatButonu = ttk.Button(input_frame, text="Fiyatlari Getir", command=fiyatlari_getir)
    fiyatButonu.grid(row=2, column=0)

    #sonuç yazısı
    sonucLabel = ttk.Label(input_frame, text="", foreground="blue")
    sonucLabel.grid(row=3, column=0, columnspan=3)
    
    #----------------- Sol üst: input frame olacak, restoran ve konum girdileri alınacak------------------------

    # ----------Sol orta: Menü Framei --------------
    menu_frame = ttk.Frame(main_frame)
    menu_frame.grid(row=1, column=0, sticky="nw")
    
    # menuyu tablo seklinde implement etmek icin Treeview kullandım
    menu = ttk.Treeview(menu_frame, columns=("Yemek", "YemekSepeti", "Getir", "MigrosYemek"), show="headings")
    
    menu.heading("Yemek", text="Yemek")
    menu.heading("YemekSepeti", text="Yemeksepeti Fiyati")
    menu.heading("Getir", text="Getir Fiyati")
    menu.heading("MigrosYemek", text="MigrosYemek Fiyati")
    
    #genişlik                       #text'i ortala
    menu.column("Yemek", width=150, anchor="center")
    menu.column("YemekSepeti", width=140, anchor="center")
    menu.column("Getir", width=140, anchor="center")
    menu.column("MigrosYemek", width=140, anchor="center")
    
    menu.pack()

    #tree_select()'i çağır
    menu.bind("<<TreeviewSelect>>", yemek_sec)

    secim_frame = ttk.Frame(menu_frame)
    secim_frame.pack(fill="x")

    #secilen yemek yazısı sol altta olacak
    secilenYemekLabel= ttk.Label(secim_frame, text="Seçilen Yemek:")
    secilenYemekLabel.pack(side="left")

    selected_food_var = tk.StringVar()

    secilenYemek = ttk.Label(secim_frame, textvariable=selected_food_var, width=20)
    secilenYemek.pack(side="left")
    
    #--------yemek ekleme-çıkarma--------
    
    #cıkar
    cikarButonu = ttk.Button(secim_frame, text="-", command=yemek_sil, width=3)
    cikarButonu.pack(side="left")

    #miktar yazısı
    miktar_var = tk.IntVar(value=0)
    miktarLabel =  ttk.Label(secim_frame, textvariable=miktar_var, width=5,anchor="center")
    miktarLabel.pack(side="left")
    
    #ekle
    ekleButonu = ttk.Button(secim_frame, text="+", command=yemek_ekle, width=3)
    ekleButonu.pack(side="left")
    
    #Sepeti label olarak göster

    #sepetin içeriği string olarak depolanıyor
    sepet_icerik = tk.StringVar()
    
    sepetLabel= ttk.Label(menu_frame, textvariable=sepet_icerik, foreground="green")
    sepetLabel.pack()

    #--------yemek ekleme-çıkarma--------

    # Sol alt: Fiyatlar ve indirim ekleme

    summary_frame = ttk.Frame(main_frame)
    summary_frame.grid(row=2, column=0, sticky="nw")
    
    #yemeksepeti indirimi
    var_joker = tk.IntVar()
    
    #getir indirimi
    var_tok = tk.IntVar()
    
    #migrosYemek indirimi
    var_flas = tk.IntVar()

    ##---------indirim checkbox'ları burada olacak-------
    indirim_frame = ttk.Frame(summary_frame)
    indirim_frame.pack(anchor="w")

    jokerButon = ttk.Checkbutton(indirim_frame, text="joker", variable=var_joker, command=indirim_guncelle)
    jokerButon.pack(side=tk.LEFT, padx=5)
    
    varButon=ttk.Checkbutton(indirim_frame, text="tok", variable=var_tok, command=indirim_guncelle)
    varButon.pack(side=tk.LEFT, padx=5)
    
    flasButon=ttk.Checkbutton(indirim_frame, text="flaş", variable=var_flas, command=indirim_guncelle)
    flasButon.pack(side=tk.LEFT, padx=5)
    ###---------indirim checkbox'ları burada olacak-------

    ##-------------fiyatların sergilenmesi-----------
    yemeksepeti_fiyatlarLabel = ttk.Label(summary_frame, text="Yemeksepeti: Toplam 0 TL, İndirim 0 TL, İndirimli 0 TL", foreground="purple")
    yemeksepeti_fiyatlarLabel.pack(anchor="w")
    
    getir_fiyatlarLabel = ttk.Label(summary_frame, text="Getir: Toplam 0 TL, İndirim 0 TL, İndirimli 0 TL", foreground="purple")
    getir_fiyatlarLabel.pack(anchor="w")
    
    migrosYemek_fiyatlarLabel = ttk.Label(summary_frame, text="MigrosYemek: Toplam 0 TL, İndirim 0 TL, İndirimli 0 TL", foreground="purple")
    migrosYemek_fiyatlarLabel.pack(anchor="w")
    #-------------fiyatların sergilenmesi-----------

    # Sağ tarafta: Favoriler listesi
    favorites_frame = ttk.Frame(main_frame)
    favorites_frame.grid(row=0, column=1, rowspan=3, sticky="nw")
    
    #Favoriler başlığı
    favorilerLabel = ttk.Label(favorites_frame, text="Favoriler")
    favorilerLabel.pack()

    #favori listesi
    favorites_list = tk.Listbox(favorites_frame, width=30, height=20)
    favorites_list.pack(padx=20)
    #favori secilince favori_sec methodunu çağır
    favorites_list.bind("<<ListboxSelect>>", favori_sec)
    favorileri_yaz()
    
    guncelle_sepet()

    def on_closing():
        empty_df = pd.DataFrame(columns=["food", "Yemeksepeti", "Getir", "MigrosYemek"])
        empty_df.to_csv("secilen.csv", index=False)
        master.destroy()

    master.protocol("WM_DELETE_WINDOW", on_closing)
    master.mainloop()