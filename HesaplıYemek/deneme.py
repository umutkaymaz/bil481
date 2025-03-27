from merge import menu_al
import config
import tkinter as tk
from tkinter import ttk
config.konum_girisi = ttk.Entry()
config.restoran_girisi = ttk.Entry()
config.konum_girisi.insert(0,"Söğütözü, Söğütözü Cd. No:43, 06510 Çankaya/Ankara")
config.restoran_girisi.insert(0,"Saray Döner")
df = menu_al("taslak.csv")
print(df)