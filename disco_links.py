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
import re
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
from unidecode import unidecode

#This funcs gives the section_urls

#This funcs gives the section_urls

def get_urls():
    #PATH = 'C:\Program Files (x86)\chromedriver.exe'
    PATH = '/usr/lib/chromium-browser/chromedriver'

    link = 'https://www.disco.com.ar/'

    s= Service(PATH)

    driver=webdriver.Chrome(service=s)
    #driver=webdriver.Firefox()

    driver.maximize_window()
    #driver.minimize_window()

    driver.get(link)
    
    
    #driver.execute_script("document.body.style.zoom='90%'") #minimize


    time.sleep(16)
#cancel button
    #driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()

    time.sleep(6)
    menu_button=driver.find_element(By.CLASS_NAME,'pr9.items-stretch.vtex-flex-layout-0-x-stretchChildrenWidth').click()


    time.sleep(5)
    iframe=driver.find_element(By.CLASS_NAME,'vtex-menu-2-x-submenu--department-menu')

    categories = driver.find_elements(By.CSS_SELECTOR,'li.vtex-menu-2-x-menuItem.vtex-menu-2-x-menuItem--menu-item-secondary')

    
    print(f' the len of categories {len(categories)}')

    full_link=[]
    categorias=[] 
    for i in categories[1:]: #preprocessing porque con chrome webdriver no se pueden clickear algunas cosas
        print(i.text)           #avoid first element cause it's different
        categorias.append(i.text)       
        elemento=unidecode(i.text).lower()
        end_link= '?map=category-1'
        if " " in elemento:
            sub=elemento.split(" ")

            substring="-".join(sub)
            
            full_link.append(link+substring+end_link) #sumo link y la parte de la categoria

        else:
            full_link.append(link+elemento+end_link)
    
    

    driver.quit()

    return categorias,full_link

section_links= get_urls()

disco = pd.DataFrame({'categorias': section_links[0],'links':section_links[1]})


today = date.today() #hold the date
d1 = today.strftime("%Y%m%d") 
disco.to_csv(f'./csv/disco/{d1}disco_links.csv', encoding='utf-8', index=False) #always printing the date of the csv file