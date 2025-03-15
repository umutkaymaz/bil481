import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import indirimhesabi  # İndirim hesaplamalari için modül

MENU_DOSYA = "menu.csv"
SECILEN_DOSYA = "secilen.csv"

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

def on_tree_select(event):
    """Seçilen menü öğesinin adini, miktar kontrol alanina aktarir."""
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        food = item["values"][0]
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
        basket[food] = basket.get(food, 0) - 1
    quantity_var.set(basket.get(food, 0))
    update_basket_csv()

# Checkbutton'larla indirim oranlarini ayarlama
def update_discounts():
    global discount_yemeksepeti, discount_getir, discount_trendyol
    discount_yemeksepeti = 1 if var_joker.get() == 1 else 0.0
    discount_getir = 1 if var_tok.get() == 1 else 0.0
    discount_trendyol = 1 if var_flas.get() == 1 else 0.0
    update_summary()

def run_gui():
    global result_label, location_entry, restaurant_entry, tree, sepet_text, root
    global summary_yemeksepeti_label, summary_getir_label, summary_trendyol_label
    global var_joker, var_tok, var_flas, selected_food_var, quantity_var

    root = tk.Tk()
    root.title("HesapliYemek")
    root.geometry("1100x800")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    # Adres ve restoran girişleri
    ttk.Label(frame, text="Adres:").grid(row=0, column=0, sticky=tk.W)
    location_entry = ttk.Entry(frame)
    location_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(frame, text="Restoran:").grid(row=1, column=0, sticky=tk.W)
    restaurant_entry = ttk.Entry(frame)
    restaurant_entry.grid(row=1, column=1, padx=5, pady=5)

    fetch_button = ttk.Button(frame, text="Fiyatlari Getir", command=fetch_prices)
    fetch_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Checkbutton'larin bulunduğu alan (Fiyatlari Getir butonunun altinda)
    discount_checkbox_frame = ttk.Frame(frame, padding=10)
    discount_checkbox_frame.grid(row=3, column=0, columnspan=2, sticky="w")
    var_joker = tk.IntVar()
    var_tok = tk.IntVar()
    var_flas = tk.IntVar()
    ttk.Checkbutton(discount_checkbox_frame, text="joker", variable=var_joker, command=update_discounts).pack(side=tk.LEFT, padx=5)
    ttk.Checkbutton(discount_checkbox_frame, text="tok", variable=var_tok, command=update_discounts).pack(side=tk.LEFT, padx=5)
    ttk.Checkbutton(discount_checkbox_frame, text="flaş", variable=var_flas, command=update_discounts).pack(side=tk.LEFT, padx=5)

    result_label = ttk.Label(frame, text="", foreground="blue")
    result_label.grid(row=4, column=0, columnspan=2)

    # Treeview: Menü listesi
    tree = ttk.Treeview(frame, columns=("Yemek", "YemekSepeti", "Getir", "Trendyol"), show="headings")
    tree.heading("Yemek", text="Yemek")
    tree.heading("YemekSepeti", text="Yemeksepeti Fiyati")
    tree.heading("Getir", text="Getir Fiyati")
    tree.heading("Trendyol", text="Trendyol Fiyati")
    tree.column("Yemek", width=150, anchor="center")
    tree.column("YemekSepeti", width=120, anchor="center")
    tree.column("Getir", width=120, anchor="center")
    tree.column("Trendyol", width=120, anchor="center")
    tree.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Miktar kontrol alani: seçilen öğe adi, "-" butonu, miktar etiketi, "+" butonu
    quantity_frame = ttk.Frame(frame, padding=10)
    quantity_frame.grid(row=6, column=0, columnspan=2, sticky="w")
    ttk.Label(quantity_frame, text="Seçilen Yemek:").pack(side=tk.LEFT)
    selected_food_var = tk.StringVar()
    ttk.Label(quantity_frame, textvariable=selected_food_var, width=20).pack(side=tk.LEFT, padx=5)
    ttk.Button(quantity_frame, text="-", command=minus_action, width=3).pack(side=tk.LEFT)
    quantity_var = tk.IntVar(value=0)
    ttk.Label(quantity_frame, textvariable=quantity_var, width=5).pack(side=tk.LEFT, padx=5)
    ttk.Button(quantity_frame, text="+", command=plus_action, width=3).pack(side=tk.LEFT)

    # Sepet gösterimi (basket listesi)
    sepet_label = ttk.Label(frame, text="Sepet (Yemek: Miktar):")
    sepet_label.grid(row=7, column=0, sticky=tk.W)
    sepet_text = tk.StringVar()
    ttk.Label(frame, textvariable=sepet_text, foreground="green").grid(row=7, column=1, sticky=tk.W)

    # Özet (Summary) alani
    summary_frame = ttk.Frame(frame, padding=10)
    summary_frame.grid(row=8, column=0, columnspan=2, sticky="nsew")
    summary_yemeksepeti_label = ttk.Label(summary_frame, text="Yemeksepeti: Toplam 0 TL, İndirim 0 TL, İndirimli 0 TL", foreground="purple")
    summary_yemeksepeti_label.pack(anchor="w")
    summary_getir_label = ttk.Label(summary_frame, text="Getir: Toplam 0 TL, İndirim 0 TL, İndirimli 0 TL", foreground="purple")
    summary_getir_label.pack(anchor="w")
    summary_trendyol_label = ttk.Label(summary_frame, text="Trendyol: Toplam 0 TL, İndirim 0 TL, İndirimli 0 TL", foreground="purple")
    summary_trendyol_label.pack(anchor="w")

    guncelle_sepet()

    def on_closing():
        empty_df = pd.DataFrame(columns=["food", "Yemeksepeti", "Getir", "Trendyol"])
        empty_df.to_csv(SECILEN_DOSYA, index=False)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
