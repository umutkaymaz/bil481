import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import indirimhesabi  # İndirim hesaplamalari için modül

MENU_DOSYA = "menu.csv"
SECILEN_DOSYA = "secilen.csv"
FAVORI_DOSYA = "favori.csv"  # Favori restoranlar için

# Global veriler
basket = {}      # { "yemek_adi": miktar }
menu_data = {}   # { "yemek_adi": { "food": ..., "Yemeksepeti": ..., "Getir": ..., "Trendyol": ... } }

# Global indirim oranlari (başlangiçta indirim uygulanmasin)
discount_yemeksepeti = 0.0
discount_getir = 0.0
discount_trendyol = 0.0

def update_basket_csv():
    """Basket sözlüğündeki her öğeyi, miktari kadar tekrarli satir olarak secilen.csv'ye yazar."""
    rows = []
    for food, qty in basket.items():
        if food in menu_data:
            data = menu_data[food]
            for _ in range(qty):
                rows.append(data)
    df = pd.DataFrame(rows, columns=["food", "Yemeksepeti", "Getir", "Trendyol"])
    df.to_csv(SECILEN_DOSYA, index=False)
    guncelle_sepet()

def guncelle_sepet():
    """Basket içeriğini GUI'de günceller ve özet hesaplamasini yapar."""
    text = "\n".join([f"{food}: {qty}" for food, qty in basket.items() if qty > 0])
    sepet_text.set(text)
    update_summary()

def update_summary():
    """Basket'teki ürünlerin her site için toplam fiyati, indirim miktari ve indirimli fiyatini hesaplar."""
    global discount_yemeksepeti, discount_getir, discount_trendyol
    total_yemeksepeti = 0
    total_getir = 0
    total_trendyol = 0
    for food, qty in basket.items():
        if food in menu_data:
            prices = menu_data[food]
            total_yemeksepeti += prices["Yemeksepeti"] * qty
            total_getir += prices["Getir"] * qty
            total_trendyol += prices["Trendyol"] * qty

    t_yemek, disc_yemek, discounted_yemek = indirimhesabi.hesapla_indirim(total_yemeksepeti, discount_yemeksepeti, 1)
    t_getir, disc_getir, discounted_getir = indirimhesabi.hesapla_indirim(total_getir, discount_getir, 2)
    t_trendyol, disc_trendyol, discounted_trendyol = indirimhesabi.hesapla_indirim(total_trendyol, discount_trendyol, 3)

    summary_yemeksepeti_label.config(text=f"Yemeksepeti: Toplam {t_yemek} TL, İndirim {disc_yemek} TL, İndirimli {discounted_yemek} TL")
    summary_getir_label.config(text=f"Getir: Toplam {t_getir} TL, İndirim {disc_getir} TL, İndirimli {discounted_getir} TL")
    summary_trendyol_label.config(text=f"Trendyol: Toplam {t_trendyol} TL, İndirim {disc_trendyol} TL, İndirimli {discounted_trendyol} TL")

def fetch_prices():
    global menu_data
    location = location_entry.get()
    restaurant = restaurant_entry.get()
    if not location or not restaurant:
        result_label.config(text="Lütfen adres ve restoran giriniz.")
        return
    try:
        df = pd.read_csv(MENU_DOSYA)
    except FileNotFoundError:
        result_label.config(text="menu.csv bulunamadi!")
        return
    tree.delete(*tree.get_children())
    menu_data = {}
    for _, row in df.iterrows():
        food = row["food"]
        prices = {"food": food, "Yemeksepeti": row["Yemeksepeti"], "Getir": row["Getir"], "Trendyol": row["Trendyol"]}
        menu_data[food] = prices
        tree.insert("", "end", values=(food, prices["Yemeksepeti"], prices["Getir"], prices["Trendyol"]))
    result_label.config(text=f"{restaurant}, {location} için sonuçlar")
    
    # Favori kontrolü: Eğer favori.csv'de bu restoran varsa, checkbox işaretlensin.
    try:
        fav_df = pd.read_csv(FAVORI_DOSYA)
        if ((fav_df["Konum"] == location) & (fav_df["Restoran"] == restaurant)).any():
            favorite_var.set(1)
        else:
            favorite_var.set(0)
    except FileNotFoundError:
        favorite_var.set(0)
    
    load_favorites()

def on_tree_select(event):
    """Seçilen menü öğesinin adini, miktar kontrol alanina aktarir."""
    selected = tree.selection()
    if selected:
        food = tree.item(selected[0])["values"][0]
        selected_food_var.set(food)
        quantity_var.set(basket.get(food, 0))

def plus_action():
    food = selected_food_var.get()
    if not food:
        return
    basket[food] = basket.get(food, 0) + 1
    quantity_var.set(basket[food])
    update_basket_csv()

def minus_action():
    food = selected_food_var.get()
    if not food:
        return
    if basket.get(food, 0) > 0:
        basket[food] -= 1
    quantity_var.set(basket.get(food, 0))
    update_basket_csv()

def update_discounts():
    global discount_yemeksepeti, discount_getir, discount_trendyol
    discount_yemeksepeti = 1 if var_joker.get() == 1 else 0.0
    discount_getir = 1 if var_tok.get() == 1 else 0.0
    discount_trendyol = 1 if var_flas.get() == 1 else 0.0
    update_summary()

def toggle_favorite():
    """Favori checkbox işaretlendiğinde veya kaldırıldığında favori.csv'yi günceller."""
    location = location_entry.get().strip()
    restaurant = restaurant_entry.get().strip()
    if not location or not restaurant:
        return
    try:
        df = pd.read_csv(FAVORI_DOSYA)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Konum", "Restoran"])
    if favorite_var.get() == 1:  # Ekleme durumu
        if not (((df["Konum"] == location) & (df["Restoran"] == restaurant)).any()):
            new_row = pd.DataFrame([[location, restaurant]], columns=["Konum", "Restoran"])
            df = pd.concat([df, new_row], ignore_index=True)
    else:  # Kaldırma durumu
        df = df[~((df["Konum"] == location) & (df["Restoran"] == restaurant))] 
    df.to_csv(FAVORI_DOSYA, index=False)
    load_favorites()

def load_favorites():
    """Favori.csv dosyasindaki favorileri liste kutusuna yükler."""
    favorites_list.delete(0, tk.END)
    try:
        df = pd.read_csv(FAVORI_DOSYA)
        for _, row in df.iterrows():
            fav_entry = f"{row['Konum']} - {row['Restoran']}"
            favorites_list.insert(tk.END, fav_entry)
    except FileNotFoundError:
        pass

def favorites_select(event):
    """Favoriler listesinde seçilen favoriyi alır ve konum ile restoran alanlarını doldurur."""
    selection = favorites_list.curselection()
    if selection:
        fav = favorites_list.get(selection[0])
        parts = fav.split(" - ")
        if len(parts) == 2:
            location_entry.delete(0, tk.END)
            location_entry.insert(0, parts[0])
            restaurant_entry.delete(0, tk.END)
            restaurant_entry.insert(0, parts[1])
            fetch_prices()

def run_gui():
    global result_label, location_entry, restaurant_entry, tree, sepet_text, root
    global summary_yemeksepeti_label, summary_getir_label, summary_trendyol_label
    global var_joker, var_tok, var_flas, selected_food_var, quantity_var, favorite_var, favorites_list

    root = tk.Tk()
    root.title("HesapliYemek")
    root.geometry("1200x800")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Sol üst: Giriş alanlari ve favori checkboxu
    input_frame = ttk.Frame(main_frame, padding=10)
    input_frame.grid(row=0, column=0, sticky="nw")
    ttk.Label(input_frame, text="Adres:").grid(row=0, column=0, sticky=tk.W)
    location_entry = ttk.Entry(input_frame)
    location_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(input_frame, text="Restoran:").grid(row=1, column=0, sticky=tk.W)
    restaurant_entry = ttk.Entry(input_frame)
    restaurant_entry.grid(row=1, column=1, padx=5, pady=5)
    favorite_var = tk.IntVar()
    favorite_checkbox = ttk.Checkbutton(input_frame, text="Favorile", variable=favorite_var, command=toggle_favorite)
    favorite_checkbox.grid(row=1, column=2, padx=5, pady=5)
    fetch_button = ttk.Button(input_frame, text="Fiyatlari Getir", command=fetch_prices)
    fetch_button.grid(row=2, column=0, columnspan=2, pady=10)
    result_label = ttk.Label(input_frame, text="", foreground="blue")
    result_label.grid(row=3, column=0, columnspan=3)

    # Sol orta: Menü listesi ve miktar kontrol alanı
    menu_frame = ttk.Frame(main_frame, padding=10)
    menu_frame.grid(row=1, column=0, sticky="nw")
    tree = ttk.Treeview(menu_frame, columns=("Yemek", "YemekSepeti", "Getir", "Trendyol"), show="headings")
    tree.heading("Yemek", text="Yemek")
    tree.heading("YemekSepeti", text="Yemeksepeti Fiyati")
    tree.heading("Getir", text="Getir Fiyati")
    tree.heading("Trendyol", text="Trendyol Fiyati")
    tree.column("Yemek", width=150, anchor="center")
    tree.column("YemekSepeti", width=120, anchor="center")
    tree.column("Getir", width=120, anchor="center")
    tree.column("Trendyol", width=120, anchor="center")
    tree.pack(pady=10)
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    quantity_frame = ttk.Frame(menu_frame, padding=10)
    quantity_frame.pack(fill=tk.X)
    ttk.Label(quantity_frame, text="Seçilen Yemek:").pack(side=tk.LEFT)
    selected_food_var = tk.StringVar()
    ttk.Label(quantity_frame, textvariable=selected_food_var, width=20).pack(side=tk.LEFT, padx=5)
    ttk.Button(quantity_frame, text="-", command=minus_action, width=3).pack(side=tk.LEFT)
    quantity_var = tk.IntVar(value=0)
    ttk.Label(quantity_frame, textvariable=quantity_var, width=5).pack(side=tk.LEFT, padx=5)
    ttk.Button(quantity_frame, text="+", command=plus_action, width=3).pack(side=tk.LEFT)
    sepet_text = tk.StringVar()
    ttk.Label(menu_frame, textvariable=sepet_text, foreground="green").pack()

    # Sol alt: Özet (Summary) ve indirim checkbutton'lari
    summary_frame = ttk.Frame(main_frame, padding=10)
    summary_frame.grid(row=2, column=0, sticky="nw")
    var_joker = tk.IntVar()
    var_tok = tk.IntVar()
    var_flas = tk.IntVar()
    discount_checkbox_frame = ttk.Frame(summary_frame, padding=10)
    discount_checkbox_frame.pack(anchor="w")
    ttk.Checkbutton(discount_checkbox_frame, text="joker", variable=var_joker, command=update_discounts).pack(side=tk.LEFT, padx=5)
    ttk.Checkbutton(discount_checkbox_frame, text="tok", variable=var_tok, command=update_discounts).pack(side=tk.LEFT, padx=5)
    ttk.Checkbutton(discount_checkbox_frame, text="flaş", variable=var_flas, command=update_discounts).pack(side=tk.LEFT, padx=5)
    summary_yemeksepeti_label = ttk.Label(summary_frame, text="Yemeksepeti: Toplam 0 TL, İndirim 0 TL, İndirimli 0 TL", foreground="purple")
    summary_yemeksepeti_label.pack(anchor="w")
    summary_getir_label = ttk.Label(summary_frame, text="Getir: Toplam 0 TL, İndirim 0 TL, İndirimli 0 TL", foreground="purple")
    summary_getir_label.pack(anchor="w")
    summary_trendyol_label = ttk.Label(summary_frame, text="Trendyol: Toplam 0 TL, İndirim 0 TL, İndirimli 0 TL", foreground="purple")
    summary_trendyol_label.pack(anchor="w")

    # Sağ tarafta: Favoriler listesi (Favoriler) - Favori restoranlar burada görünecek
    favorites_frame = ttk.Frame(main_frame, padding=10)
    favorites_frame.grid(row=0, column=1, rowspan=3, sticky="n")
    ttk.Label(favorites_frame, text="Favoriler", foreground="brown").pack()
    favorites_list = tk.Listbox(favorites_frame, width=30, height=20)
    favorites_list.pack(padx=5, pady=5)
    favorites_list.bind("<<ListboxSelect>>", favorites_select)
    load_favorites()
    
    guncelle_sepet()

    def on_closing():
        empty_df = pd.DataFrame(columns=["food", "Yemeksepeti", "Getir", "Trendyol"])
        empty_df.to_csv(SECILEN_DOSYA, index=False)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    run_gui()

