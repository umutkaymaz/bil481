from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Use Chrome options
import undetected_chromedriver as uc
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random

def getiryemek_restaurant_scrape(address, query):

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options)
    
    driver.get("https://getir.com/yemek/")
    
    time.sleep(3)

    div1 = driver.find_element(by="xpath", value='//div[contains(@class, "iyWiNv")]')
    div1_1 = div1.find_element(by="xpath", value='.//div[contains(@data-testid, "input")]')
    driver.execute_script("arguments[0].click();", div1_1.find_element(by="xpath", value='.//input'))
    time.sleep(5)
    div2 = driver.find_element(by="xpath", value='//div[contains(@class, "eSQuof")]')
    div2_input = div2.find_element(by="xpath", value='.//input')
    driver.execute_script("arguments[0].click();", div2_input)
    #driver.execute_script("arguments[0].value = arguments[1];", div2_input, address)
    div2_input.click()
    div2_input.send_keys(address)
    time.sleep(5)
    div3 = driver.find_element(by="xpath", value='//div[contains(@class, "fukqqF")]')
    driver.execute_script("arguments[0].click();", div3.find_element(by="xpath", value='.//button'))
    time.sleep(2)
    div4 = driver.find_element(by="xpath", value='//div[contains(@class, "gKCsjQ")]')
    driver.execute_script("arguments[0].click();", div4.find_element(by="xpath", value='.//button'))
    time.sleep(2)
    div5 = driver.find_element(by="xpath", value='//div[contains(@class, "gXXFfv")]')
    driver.execute_script("arguments[0].click();", div5.find_element(by="xpath", value='.//button'))
    time.sleep(2)
    div6 = driver.find_element(by="xpath", value='//div[contains(@class, "ezpKor")]')
    driver.execute_script("arguments[0].click();", div6.find_element(by="xpath", value='.//button'))

    time.sleep(8)

    found = False
    while True:
        # Get list of currently loaded restaurants

        restaurant_elements = driver.find_elements(by="xpath", value='/html/body/div[1]/div[3]/main/div/section/section[3]/div/section/article//p')

        print(len(restaurant_elements))

        for restaurant in restaurant_elements:
            name = restaurant.text
            
            if is_matching_restaurant(name, query):
                driver.execute_script("arguments[0].click();", restaurant)  # Open the restaurant page
                time.sleep(2)  # Allow time for page load
                found = True
                break

        if found: 
            break
        # Try clicking "Load More"
        try:
            button_section = driver.find_element(by="xpath", value='//div[contains(@class, "kCcmYM")]')
            button = button_section.find_element(by="xpath", value='.//button')
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)  # Wait for new restaurants to load
        except:
            print("No more restaurants to load.")
            break  # Stop if button is gone
    if found:
        dish_names = []
        dish_prices = []

        minimum_value = driver.find_element(by="xpath", value='/html/body/div[1]/div[2]/main/div/div/div/div[1]/div/div/div[2]/div[3]/div/article[2]/div[2]/div/div/span').text
        minimum_value = minimum_value[minimum_value.find("₺"):].replace(",",".")

        info = pd.DataFrame({"Getiryemek_minimum" : minimum_value})
        info.to_csv("./getiryemek_info.csv")

        menu = driver.find_element(by="xpath", value='/html/body/div[1]/div[3]/main/div/div/div/div[3]/div[2]/div/div[2]')
        sub_menus = menu.find_elements(by="xpath", value='./div')
        for sub_menu in sub_menus:
            if sub_menu.find_element(by="xpath", value='./h3').text != "En Sevilenler":
                dishes = sub_menu.find_elements(by="xpath", value='./div')
                for dish in dishes:
                    dish_name = dish.find_element(by="xpath", value='.//h4[contains(@data-testid, "title")]').text
                    if dish_name.find("(") > -1:
                        dish_name = dish_name[:dish_name.find("(") - 1]
                    dish_names.append(dish_name)
                    dish_price = dish.find_element(by="xpath", value='.//span[contains(@data-testid, "text")]').text
                    dish_price = dish_price.replace(",", ".")[1:]
                    dish_prices.append(dish_price)

        df = pd.DataFrame({"Name" : dish_names, "Price" : dish_prices})
        df.to_csv("./webScraping_TEST/getiryemekSCRAPED.csv")
    driver.quit()
            



def is_matching_restaurant(restaurant_name, query):
    if restaurant_name.find(query) > -1:
        return True
    return False

