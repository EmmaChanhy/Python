#pip install selenium

from operator import index
import pandas as pd
from tkinter import Menu
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
import os

chrome_driver_path = "/Users/emma/Desktop/Python_Projects/Selenium/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

#Get the time now
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

#Go to google
driver.get("https://www.google.com/")

#Click 'I agree'
driver.find_element(By.CSS_SELECTOR, "#L2AGLb > div").click()

#Search 'btc price'
google_search = driver.find_element(by=By.NAME, value="q")
google_search.send_keys("btc price")
google_search.send_keys(Keys.ENTER)

#Click coinmarketcap
coinmarkcap = driver.find_element(by=By.XPATH,value='//a[starts-with(@href,"https://coinmarketcap.com")]')
coinmarkcap.click()

#Get BTC Price
driver.get("https://coinmarketcap.com/currencies/bitcoin/")
btc_price = driver.find_element(by=By.CLASS_NAME,value="priceValue").text
btc_time_price = {dt_string:btc_price}

#Export df to csv
btc_csv_path = '/Users/emma/Desktop/Python_Projects/Selenium/btc_price.csv'
files = os.listdir(os.path.expanduser('/Users/emma/Desktop/Python_Projects/Selenium'))
if 'btc_price.csv' in files:
    btc_csv_df = pd.read_csv(btc_csv_path)
    btc_csv_df = btc_csv_df.append({'Timestamp':dt_string,'btc_price':btc_price},ignore_index=True)
    btc_csv_df.to_csv(btc_csv_path, index=False)
    print('Successfully append btc price to existing csv')
else:
    df = pd.DataFrame(columns=['Timestamp', 'btc_price'])
    df = df.append({'Timestamp':dt_string,'btc_price':btc_price},ignore_index=True)
    df.to_csv(btc_csv_path, index=False)
    print('Successfully export to csv')

driver.quit()
