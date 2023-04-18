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


#This funcs gives the section_urls

def get_urls():
    #PATH = 'C:\Program Files (x86)\chromedriver.exe'

    PATH= '/usr/lib/chromium-browser/chromedriver'

    link = 'https://www.jumbo.com.ar/'

    s= Service(PATH)

    driver=webdriver.Chrome(service=s)

    driver.maximize_window()

    driver.get(link)
    time.sleep(16)
#cancel button
    #driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()

    time.sleep(6)
    menu_button=driver.find_element(By.CLASS_NAME,'pr9.items-stretch.vtex-flex-layout-0-x-stretchChildrenWidth').click()


    time.sleep(5)
    iframe=driver.find_element(By.CLASS_NAME,'vtex-menu-2-x-submenu--department-menu')

    categories = driver.find_elements(By.CSS_SELECTOR,'li.vtex-menu-2-x-menuItem.vtex-menu-2-x-menuItem--menu-item-secondary')

    print(f' the len of categories {len(categories)}')
    
    

    links=[]
    for i in range(1,len(categories)-1):
        time.sleep(2)
        categories = driver.find_elements(By.CSS_SELECTOR,'li.vtex-menu-2-x-menuItem.vtex-menu-2-x-menuItem--menu-item-secondary')
        time.sleep(7)
        #action=ActionChains(driver)
        #action.move_to_element(categories[i]).perform()
        driver.execute_script("arguments[0].scrollIntoView();", categories[i])
        time.sleep(5)
        #action.click(categories[i]).perform()
        categories[i].click()
        time.sleep(1)
        url= driver.current_url
        links.append(url)
        time.sleep(6)
        
        menu_button=driver.find_element(By.CLASS_NAME,'pr9.items-stretch.vtex-flex-layout-0-x-stretchChildrenWidth')
        time.sleep(3)
        menu_button.click()
        time.sleep(2)
        #action.move_to_element(categories[14]).perform()
        #driver.execute_script("arguments[0].scrollIntoView();", categories[14])

    driver.quit()

    return links


section_links= get_urls() #applying the func to get section urls


#this funcs gives the func to analyze

def urls_analyze(link):

    links=link

    #PATH = 'C:\Program Files (x86)\chromedriver.exe'

    PATH= '/usr/lib/chromium-browser/chromedriver'



    s= Service(PATH)

    driver=webdriver.Chrome(service=s)

    driver.maximize_window()

    driver.get(links)
    time.sleep(15)


#cancel button
    #driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,'div.categoryList-box')
    driver.implicitly_wait(2)
    driver.find_element(By.CSS_SELECTOR,'.categoryList__viewAll').click()
    time.sleep(3)
   

    return driver.current_url


getting_urls=[urls_analyze(i) for i in section_links] #applying the second func


jumbo= pd.DataFrame({'links': getting_urls})

today = date.today() #hold the date
d1 = today.strftime("%Y%m%d") 
jumbo.to_csv(f'./csv/jumbo/{d1}jumbo_links.csv', encoding='utf-8', index=False) #always printing the date of the csv file