import tkinter as tk
from tkinter import ttk
import pandas as pd
from indirimhesabi import fiyatlari_hesapla
from GUI_actions import yemek_ekle
from GUI_actions import yemek_sil
from GUI_actions import yemek_sec
from GUI_actions import favorileri_yaz
from GUI_actions import favori_sec
from GUI_actions import favori_guncelle
from GUI_actions import fiyatlari_getir

#run_GUI da oluşturduğum global değişkenleri (GUI elemanları (Labellar etc.)) 
#diğer modüller tarafında erişilebilir kılıyorum   

#sepeti bir dictionary de tutuyoruz. {yemek_adı : yemek_miktarı}
sepet = {}

menu_data = {}   


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
    
    #favorite_var = 1 ise chechkbox isaretli degil ise 0
    favorite_var = tk.IntVar()
    
    #toogle_favorite() çağır
    favori_checkbox = ttk.Checkbutton(input_frame, text="Favori", variable=favorite_var, command=favori_guncelle)
    favori_checkbox.grid(row=1, column=2)

    #fiyatlari_getir() çağır
    fiyatButonu = ttk.Button(input_frame, text="Fiyatlari Getir", command= lambda : fiyatlari_getir(menu_data,favorite_var))
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
    menu.bind("<<TreeviewSelect>>", lambda event :  yemek_sec(event, sepet, selected_food_var, miktar_var))

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
    cikarButonu = ttk.Button(secim_frame, text="-", command=lambda : yemek_sil(var_joker.get(), var_tok.get(), var_flas.get(),
                            sepet_icerik,selected_food_var,sepet, miktar_var, menu_data), width=3)
    cikarButonu.pack(side="left")

    #miktar yazısı
    miktar_var = tk.IntVar(value=0)
    miktarLabel =  ttk.Label(secim_frame, textvariable=miktar_var, width=5,anchor="center")
    miktarLabel.pack(side="left")
    
    #ekle
    ekleButonu = ttk.Button(secim_frame, text="+", command= lambda : yemek_ekle(var_joker.get(), var_tok.get(), var_flas.get(),
                            sepet_icerik,selected_food_var,sepet, miktar_var, menu_data), width=3)
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

    jokerButon = ttk.Checkbutton(indirim_frame, text="joker", variable=var_joker, command= lambda : fiyatlari_hesapla(var_joker.get(),var_tok.get(),var_flas.get(),sepet,menu_data))
    jokerButon.pack(side=tk.LEFT, padx=5)
    
    varButon=ttk.Checkbutton(indirim_frame, text="tok", variable=var_tok, command= lambda : fiyatlari_hesapla(var_joker.get(),var_tok.get(),var_flas.get(),sepet,menu_data))
    varButon.pack(side=tk.LEFT, padx=5)
    
    flasButon=ttk.Checkbutton(indirim_frame, text="flaş", variable=var_flas, command= lambda : fiyatlari_hesapla(var_joker.get(),var_tok.get(),var_flas.get(),sepet,menu_data))
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
    favorites_list.bind("<<ListboxSelect>>", lambda event : favori_sec(event,menu_data,favorite_var))
    favorileri_yaz()

    def on_closing():
        empty_df = pd.DataFrame(columns=["food", "Yemeksepeti", "Getir", "MigrosYemek"])
        empty_df.to_csv("secilen.csv", index=False)
        master.destroy()

    master.protocol("WM_DELETE_WINDOW", on_closing)
    master.mainloop()