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


def info():

    #PATH= 'C:\Program Files (x86)\chromedriver.exe'
    
    PATH= '/usr/lib/chromium-browser/chromedriver'

    link = 'https://www.carrefour.com.ar/'

    s = Service(PATH)
    #options = webdriver.FirefoxOptions()
    time.sleep(1)
    #driver = webdriver.Chrome(service=s)
    #driver=webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
    #driver=webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    driver= webdriver.Chrome(service=s)
    time.sleep(1)
    driver.get(link)
    driver.maximize_window()
    time.sleep(3)
    
    time.sleep(14)

    # accept cookies consent
    consent_button = driver.find_element(By.ID,'onetrust-accept-btn-handler')
    consent_button.click()
    time.sleep(5)

    # select the left menu bar
    barra = driver.find_element(By.CSS_SELECTOR, '.vtex-store-drawer-0-x-openIconContainer--menuCategory').click()

    # select the iframe
    #iframe = driver.find_element(
    #    By.CSS_SELECTOR,'div.vtex-store-drawer-0-x-drawerContent.vtex-store-drawer-0-x-drawerContent--menuCategory.overflow-y-auto')

    iframe=driver.find_element(By.CSS_SELECTOR,'.vtex-menu-2-x-menuContainerNav.vtex-menu-2-x-menuContainerNav--MenuCategoryFirst')

#actions=ActionChains(driver)
#actions.move_to_element(iframe).perform()
    time.sleep(2)
# find the menu links
    menu=driver.find_elements(By.CLASS_NAME,'vtex-menu-2-x-styledLinkContent.vtex-menu-2-x-styledLinkContent--MenuCategoryFirstItem')
#actions.move_to_element(menu[1]).perform()
#time.sleep(2)
        
    print(f'cantidad de columnas: {len(menu)}')
    
    tablas=[]
    subtablas=[]
    links=[]

    for i in range(len(menu)):
        
        driver.execute_script("arguments[0].scrollIntoView();",menu[i])
        
        time.sleep(1)
        #ActionChains(driver).move_to_element(i).perform()
        time.sleep(1)
        menu[i].click()
        menu[i].click()
        #driver.execute_script("arguments[0].click();", menu[i])
    
    
    
        time.sleep(3)

        sub_menu=driver.find_elements(By.CSS_SELECTOR,'.vtex-menu-2-x-styledLinkContainer.vtex-menu-2-x-styledLinkContainer--MenuCategorySecondItem-hasSubmenu.mh6.pv2')
    
        #create elements for the tablas
        categories_title= menu[i].text
        tablas.extend([categories_title]*len(sub_menu))#### Ver código abajo
    
        #how many submanus have each tabla
        print(f'{categories_title}, iteracion de categoria: {i}')
        print(f'largo de la lista: {len(sub_menu)}')
        
    
        for h in range(len(sub_menu)):
            time.sleep(4)
            print(f'itineracion n°: {h}')
            print(f'menu n°:{i}')
        
        


            sub_menu=driver.find_elements(By.CSS_SELECTOR,'.vtex-menu-2-x-styledLinkContainer.vtex-menu-2-x-styledLinkContainer--MenuCategorySecondItem-hasSubmenu.mh6.pv2')

            print(f'valores de sub menu {sub_menu[h].text}')
        #add the text title tu subtablas
            subtablas.append(sub_menu[h].text)
            time.sleep(9)
            try:
                sub_menu[h].click()
            except StaleElementReferenceException:
                sub_menu[h].click()
            url= driver.current_url
            links.append(url)
            time.sleep(8)
            driver.get(link)
            time.sleep(8)
        # get geeksforgeeks.org
        
        # try to find and click the left menu bar
            try:
                barra = driver.find_element(By.CSS_SELECTOR, '.vtex-store-drawer-0-x-openIconContainer--menuCategory').click()
            except StaleElementReferenceException:
                barra = driver.find_element(By.CSS_SELECTOR, '.vtex-store-drawer-0-x-openIconContainer--menuCategory').click()

            time.sleep(4)

            iframe=driver.find_element(By.CSS_SELECTOR,'.vtex-menu-2-x-menuContainerNav.vtex-menu-2-x-menuContainerNav--MenuCategoryFirst')
            time.sleep(2)
        # find the menu links
            menu=driver.find_elements(By.CLASS_NAME,'vtex-menu-2-x-styledLinkContent.vtex-menu-2-x-styledLinkContent--MenuCategoryFirstItem')
            menu[i].click()

        

    print('###################')

    return links,tablas,subtablas

data= info()

carrefour_main= pd.DataFrame({'links': data[0],'categories': data[1],'subcategories':data[2]})

today = date.today() #hold the date
d1 = today.strftime("%Y%m%d") 
carrefour_main.to_csv(f'./csv/carrefour/{d1}carrefour_links.csv', encoding='utf-8', index=False) #always printing the date of the csv file