import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
#time
import time
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
from unidecode import unidecode
from datetime import date
from bs4 import BeautifulSoup
import requests


def products(categoria,source):  #function for taking data for products

    

    #r = requests.get(url)


    soup =BeautifulSoup(source,'html.parser')

    #frame = soup.find('div',class_='vtex-search-result-3-x-gallery vtex-search-result-3-x-gallery--default flex flex-row flex-wrap items-stretch bn ph1 na4 pl9-l')

    #print(frame)
    
    products =soup.find_all('div',class_='vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--default pa4')
    
    count_product=0
    product_list=[]
    for product in products:
         
        count_product=count_product+1
    #this is the count fraction to check the scrapped elements
        print(f'{count_product} / {len(products)} Elemento escrapeado')

        current_product={'market':'Dia','category': categoria,'currency':'ARG'}

        #marca producto
        brand= product.find('div',class_='vtex-product-summary-2-x-productBrandContainer').text
        current_product['marca']=brand

        #precio descripcion
        description= product.find('div',class_='vtex-product-summary-2-x-nameContainer flex items-start justify-center pv6').text
        current_product['descripcion'] =description

        #promocion
        try:
            promocion= product.find('div',class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--shelf_promotions').text
            current_product['promocion'] = promocion
        except:
            current_product['promocion'] = None

        #precio producto
        precio = product.find('div',class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--shelf_prices').text
    
        if precio.count('$',2):
            part = precio.split("$")          
            precio= "$"+part[1]
            precio_promocion="$"+part[2]
        else:
            precio
            
            precio_promocion= None
        
    
        
        current_product['precio_producto'] =precio
        current_product['precio_promocion'] = precio_promocion

        #precio x unidad
        precio_unidad = product.find('div',class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--product-unit').text
        current_product['precio_kilo']= precio_unidad
        

        product_list.append(current_product)


    return product_list


def full_scrap(categoria,link):  # every page of every category


    PATH= '/usr/lib/chromium-browser/chromedriver'

    

    s= Service(PATH)

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Habilitar el modo sin cabeza
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--windows-size=1920,1080')
    #chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument('--disable-extensions')
    #chrome_options.add_argument('--start-maximized')
    #chrome_options.add_argument('--windows-size=1920,1080')
    #chrome_options.add_argument('--windows-size=1920,1080')

    driver = webdriver.Chrome(service=s,options=chrome_options)

    driver.maximize_window()

    driver.get(link)

    time.sleep(12)


    if driver.current_url=='https://diaonline.supermercadosdia.com.ar/almacen':
        elemento= driver.find_elements(By.CSS_SELECTOR,'div.vtex-search-result-3-x-filter__container.vtex-search-result-3-x-filter__container--plp')
        driver.execute_script("arguments[0].scrollIntoView(0);", elemento[5])
        time.sleep(6)

        label = driver.find_elements(By.CSS_SELECTOR,"label[for*='category-2']")
        print(len(label))

#almost done
        full=[]
        for u in label:
            try:
                g=driver.find_element(By.CSS_SELECTOR,"g[transform='translate(2 2)']")
                g.click()
                time.sleep(2)
                exit= driver.find_element(By.CSS_SELECTOR,'button[title="Close survey"]')
                exit.click()
            except:
                pass
            print(u.text)
            u.click()
            time.sleep(7)

            cont=0
            prev_url = None 
            while True:
                cont+=1
                if driver.current_url == prev_url:
            # Salir del bucle si driver.current_url no ha cambiado
                    break
    
                prev_url = driver.current_url

                print(f'cantidad de hojas: {cont}') #contador
                elemento = driver.find_element(By.CSS_SELECTOR, 'div.vtex-search-result-3-x-buttonShowMore--layout')
                driver.execute_script("arguments[0].scrollIntoView(0);", elemento) 
                time.sleep(10)

            data=products(categoria,driver.page_source) #aplico la func
            full.extend(data) #extend o append?

            elemento= driver.find_elements(By.CSS_SELECTOR,'div.vtex-search-result-3-x-filter__container.vtex-search-result-3-x-filter__container--plp')
            driver.execute_script("arguments[0].scrollIntoView(0);", elemento[5])
            time.sleep(3)
            u.click()
            time.sleep(7)
            elemento= driver.find_elements(By.CSS_SELECTOR,'div.vtex-search-result-3-x-filter__container.vtex-search-result-3-x-filter__container--plp')
            driver.execute_script("arguments[0].scrollIntoView(0);", elemento[5])
            time.sleep(6)
        df= pd.DataFrame(full).replace("", None)
        

    
    else:
        cont = 0
        prev_url = None  # Almacenar el valor anterior de driver.current_url
        while True:
    
            if driver.current_url == prev_url:
            # Salir del bucle si driver.current_url no ha cambiado
                break
    
            prev_url = driver.current_url  # Actualizar el valor anterior de driver.current_url
    
            cont=cont+1
            print(f'cantidad de hojas: {cont}')
            elemento = driver.find_element(By.CSS_SELECTOR, 'div.vtex-search-result-3-x-buttonShowMore--layout')
            driver.execute_script("arguments[0].scrollIntoView(0);", elemento)
            time.sleep(10)
    

    
        data=products(categoria,driver.page_source)

        df=pd.DataFrame(data).replace("",None)
       

    driver.quit()

    return df


# main_data= pd.read_csv('./csv/dia/20230411dia_links.csv') #loading the csv from files

# main_data= main_data.loc[1:] #take out the promo because there is another web format

# #all data
# main=[full_scrap(i,u) for i,u in zip(main_data['categoria'],main_data['links'])]

# dfs=[pd.DataFrame(i) for i in main] # creating the dataframes from each category
# df=pd.concat(dfs) #full df

# today = date.today()
# d1 = today.strftime("%Y%m%d")
# df.to_csv(f'./csv/dia/{d1}_dia_products.csv', encoding='utf-8', index=False)

