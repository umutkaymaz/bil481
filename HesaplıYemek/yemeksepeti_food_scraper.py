from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Use Chrome options
import undetected_chromedriver as uc
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import random 
from address import get_yemeksepeti_link
import os

def yemeksepeti_food_scrape(address, query):
    
    driver2 = None

    options2 = Options()
    options2.add_argument("--disable-blink-features=AutomationControlled")

    driver2 = uc.Chrome(options=options2)

    driver2.delete_all_cookies()

    q = query.replace(" ","+").lower()
    driver2.get(get_yemeksepeti_link(address) + "&query=" + q)

    time.sleep(random.uniform(3,5))

    section = driver2.find_element(by="xpath", value='//section[contains(@class, "open-section")]')

    driver2.execute_script("arguments[0].click();", section.find_element(by="xpath", value='.//a'))

    time.sleep(5)

    dishes = driver2.find_elements("xpath", '//li[contains(@data-testid, "menu-product")]')

    dish_names = []
    dish_prices = []

    for dish in dishes:
        dish_name = dish.find_element("xpath", './/span[contains(@data-testid, "menu-product-name")]').text
        if dish_name == "Poşet":
            continue
        if dish_name.find("(") > -1:
            dish_name = dish_name[:dish_name.find("(") - 1]
        dish_names.append(dish_name)
        dish_price = dish.find_element("xpath", './/p[contains(@data-testid, "menu-product-price")]').text
        dish_price = dish_price.replace(",",".")[:dish_price.find("T") - 1]
        dish_prices.append(dish_price)

    df = pd.DataFrame({"Name" : dish_names, "PriceYemek" : dish_prices})
    
    df.to_csv("Yemeksepeti.csv", index=False)

    if driver2:
        driver2.quit()
