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




def products(source,categories,subcategories): #product func that select product data


    time.sleep(1)
    section = BeautifulSoup(source)     #inition

    products = section.find_all('div', attrs={'class': 'lyracons-search-result-1-x-galleryItem'})

    print(f' cantidad de pruductos: {len(products)}')

    count_product=0
    product_list=[]
    time.sleep(1)
    for p in products:
    #counting products
        count_product=count_product+1
    #this is the count fraction to check the scrapped elements
        print(f'{count_product} / {len(products)} Elemento escrapeado')
    #this is de dictionary that store all products
        current_product={'market':'Carrefour','category': categories,
                         'subcategory':subcategories,'currency':'ARG'}
        time.sleep(1)
    #####################################################################################
    #columns to add
    ###product description
        product= p.find('span',attrs={'class': 'vtex-product-summary-2-x-productBrand'})
        current_product['descripcion_producto'] = product.text
        #print(product.text)
        
    ### price
        try: 
            part_price = p.find_all('span',attrs={'class':'lyracons-carrefourarg-product-price-1-x-currencyContainer'})
            precio = ''
            for price in part_price:
        
                precio += price.text   
            
            if precio.count('$',2):          
                precio= precio.split("$")[2]
                #print(precio)
            
            else:
                precio
                #print(precio) 

        except AttributeError:
            precio= None
            
        current_product['precio_producto'] = precio

              
        try:
            precio_promocion = p.find('span',attrs={'class':'lyracons-carrefourarg-product-price-1-x-sellingPrice'}).text
            #print(f' precio con promocion: {precio_promocion}')
            if precio != precio_promocion:
                current_product['precio_promocion']=precio_promocion
            else:
                current_product['precio_promocion'] = None
        except:
            current_product['precio_promocion'] = None
        
        try:
            descripcion_promocion = p.find('span',attrs={'class':'tooltipText'}).text
            if descripcion_promocion != None :
                current_product['descripcion_promocion'] = descripcion_promocion
            ### link to image
            img = p.find('img',attrs={'class':'vtex-product-summary-2-x-imageNormal'}).get('src')
            current_product['imagen'] =img
        except:
            current_product['descripcion_promocion'] = None
            current_product['imagen'] = None
     ### link to image
        
    ###if it has a discount
        product_list.append(current_product)
    
    
    return product_list #check the answer
    


def full_data(link,category,sub): #every page from url


    PATH= '/usr/lib/chromium-browser/chromedriver'
    s = Service(PATH)
    #options = webdriver.ChromeOptions()
    #options.add_argument('--disable-extensions')
    #options.add_argument('--disable-gpu')
    #options.add_argument('--no-sandbox')
    #options.add_argument('--headless')
    
    driver = webdriver.Chrome(service=s)
    driver.get(link)
    driver.maximize_window()

    time.sleep(14)

    # accept cookies consent
    try:
        consent_button = driver.find_element(By.ID,'onetrust-accept-btn-handler') #ver si el consent button va siempre, creo que no
        consent_button.click()

    except NoSuchElementException:
        pass
    
    time.sleep(8)


    css_selector_button = '.lyracons-search-result-1-x-paginationButtonChangePage.mr3.flex.justify-center'
    cambio_pagina = driver.find_elements(By.CSS_SELECTOR,css_selector_button)


    source=driver.page_source
    
    
    final_work=[] # list where i hold all the data
    final_work.extend(products(source,category,sub))

    try:
        print(f'page number: {2}') 
        button= driver.find_element(By.CSS_SELECTOR,'button[value="2"]')
        time.sleep(2)
        button.click()
        time.sleep(6)
        source= driver.page_source
        final_work.extend(products(source, category, sub))
    except:
        pass


    #prueba para saltear el bug
    total= driver.find_element(By.CSS_SELECTOR,'.lyracons-search-result-1-x-totalProducts--layout').text

    number = int(total.split()[0])         
        
    if number%16==0:
        number_pages= int(number/16) #hay un bug entre la hoja 1 y hoja 2 de productos que genera un error. 
    else:
        number_pages= int(number//16+1)

    print(f'Total number of products: {number}')
    print(f'number pages: {number_pages}')
    
    
    if number_pages>2: #cambio el number_page por uno mayor, asi borro

        for i in range(3,number_pages+1):  #loop de paginas
            try:
                print(f'page number: {i}') 
                button= driver.find_element(By.CSS_SELECTOR,f'button[value="{i}"]')
                time.sleep(2)
                button.click()
                time.sleep(6)
                source= driver.page_source
                final_work.extend(products(source, category, sub)) #hold the data
                time.sleep(2)
            except:
                break
    else:
        pass

    return final_work



main_data= pd.read_csv('../csv/carrefour/20230410carrefour_links.csv') #this csv file contains the
                                                                       #main categories


full = [full_data(i,u,y) for i,u,y in zip(main_data['links'],main_data['categories'],main_data['subcategories'])]


df=[]
for i in full:
    for x in i:
        row=pd.DataFrame([x])
        print(f'this is the dictionary :{x}')
        df.append(row)
        

dfs=pd.concat(df) 

dfs=dfs.reset_index().drop(columns='index') 
today = date.today() #hold the date
d1 = today.strftime("%Y%m%d") 
dfs.to_csv(f'../csv/carrefour/{d1}_carrefour_products.csv', encoding='utf-8', index=False) #always printing the date of the csv file



