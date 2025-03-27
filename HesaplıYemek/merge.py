import config
from yemeksepeti_food_scraper import yemeksepeti_food_scrape
from getiryemek_food_scraper import getiryemek_restaurant_scrape
import pandas as pd
import time

def menu_al(path_csv):
    konumx = config.konum_girisi.get()
    lokantax = config.restoran_girisi.get()
    
    yemeksepeti_food_scrape(konumx,lokantax)
    time.sleep(2)
    getiryemek_restaurant_scrape(konumx,lokantax)
    
    dfYemekSepeti = pd.read_csv("Yemeksepeti.csv")
    dfGetir = pd.read_csv("Getiryemek.csv")
    
    dfMenu = pd.merge(dfYemekSepeti,dfGetir,on="Name",how="outer")
    dfMenu.to_csv(path_csv,index=False)
    return dfMenu