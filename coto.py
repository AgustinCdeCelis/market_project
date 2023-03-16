import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException


url = 'https://www.cotodigital3.com.ar'

#this func takes the first url all with Beatiful Soup and the names, categories
def take_url():
    #taking the url
    r = requests.get(url)


    soup =BeautifulSoup(r.text,'html.parser')
    #selecting the tags
    classes=soup.find_all('ul',class_='sub_category')
    
    #looking at the href
    links= [i.find('a')['href'] for i in classes]

    #names of categories
    names=[i.a.text   for i in classes]
    #taking out the spaces and extra symbols
    names_categories = [i.replace(' (+)','').strip() for i in names]
                               
    return links ,names_categories
    
def full_urls(partial_link,names_categories):
    PATH= 'C:\Program Files (x86)\chromedriver.exe'

    link_total = 'https://www.cotodigital3.com.ar'+partial_link

    s = Service(PATH)

    driver = webdriver.Chrome(service=s)
    #driver=webdriver.Chrome()
    time.sleep(2)
    driver.get(link_total)
    time.sleep(1)
    driver.maximize_window()
    time.sleep(18)
    #next = driver.find_element(By.LINK_TEXT,'Sig')
    total_urls=[]
    total_urls.append(link_total)
    while True:
            try:
                next = driver.find_element(By.LINK_TEXT,'Sig')
                time.sleep(2)
                next.click()
                pages= driver.current_url
                total_urls.append(pages)
                time.sleep(7)
            except:
                 break
                 
                 
    sig= driver.find_elements(By.CSS_SELECTOR,'a[title*="Ir a página"]')
    
    for i in range(1,len(sig)):
        try:
            sig= driver.find_elements(By.CSS_SELECTOR,'a[title*="Ir a página"]')
            time.sleep(2)
            sig[i].click()
            pages= driver.current_url
            total_urls.append(pages)
            time.sleep(7)
        except IndexError:
            sig = driver.find_elements(By.CSS_SELECTOR,'a[title*="Ir a página"]')
            time.sleep(2)
            sig[1].click()
            pages=driver.current_url
            total_urls.append(pages)
    
    
    print(f'the total urls: {len(total_urls)}')
    print(f' the name categories: {names_categories}')
    nombre=names_categories*len(total_urls)                       

    driver.quit()

    return total_urls,nombre


