import config
from yemeksepeti_food_scraper import yemeksepeti_food_scrape
from getiryemek_food_scraper import getiryemek_restaurant_scrape
import pandas as pd

def menu_al(path_csv):
    konumx = config.konum_girisi.get()
    lokantax = config.restoran_girisi.get()
    
    dfYemekSepeti = yemeksepeti_food_scrape(konumx,lokantax)
    dfGetir = getiryemek_restaurant_scrape(konumx,lokantax)
    dfMenu = pd.merge(dfYemekSepeti,dfGetir)
    dfMenu.to_csv(path_csv)
    return dfMenu