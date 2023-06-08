import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
#time
import time
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
from unidecode import unidecode
from datetime import date


def full():

    PATH= '/usr/lib/chromium-browser/chromedriver'

    link = 'https://diaonline.supermercadosdia.com.ar/'

    s= Service(PATH)

    driver = webdriver.Chrome(service=s)

    driver.set_window_size(1366,768)

    driver.get(link)

    time.sleep(12)

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)

    buttons_a= driver.find_elements(By.CSS_SELECTOR,'div.vtex-menu-2-x-styledLinkContainer.vtex-menu-2-x-styledLinkContainer--compra-online')


    categoria=[]
    for i in buttons_a:
        #print(i.text)
        categoria.append(unidecode(i.text).lower()) #saco tildes y hago minuscula


    buttons_b= driver.find_elements(By.CSS_SELECTOR,'div.vtex-menu-2-x-styledLinkContainer.vtex-menu-2-x-styledLinkContainer--compra-online-2')

    for i in buttons_b:
        
        categoria.append(unidecode(i.text).lower()) #sacar tildes y hacerlo minuscula

    full_link=[]
    for elemento in categoria:
        if " " in elemento:
            sub=elemento.split(" ")

            substring="-".join(sub)
            if substring == 'frutas-y-verduras':
                corregido="/".join([ 'frescos','frutas-y-verduras'])
                full_link.append(link+corregido) #sumo link y la parte de la categoria
            else:

                full_link.append(link+substring) #sumo link y la parte de la categoria

        else:
            full_link.append(link+elemento)

    df = pd.DataFrame({'categoria':categoria,'links': full_link})

    return df

#data=full()


# today = date.today() #hold the date
#d1 = today.strftime("%Y%m%d") 
#data.to_csv(f'./csv/dia/{d1}dia_links.csv', encoding='utf-8', index=False) #always printing the date of the csv file
