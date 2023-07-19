import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
#time
import time
from selenium.webdriver.chrome.options import Options
import re
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date




def products(source,categories,subcategories): #product func that select product data
    print(categories)
    print(subcategories)

    time.sleep(1)
    section = BeautifulSoup(source,'html.parser')     #inition

    #products = section.find_all('div', attrs={'class': 'lyracons-search-result-1-x-galleryItem'})
    products = section.select('article.vtex-product-summary-2-x-element.vtex-product-summary-2-x-element--contentProduct')
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
    
    
    driver = webdriver.Chrome(service=s)
    driver.get(link)
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, 10)")

    time.sleep(16)

    # accept cookies consent
    try:
        consent_button = driver.find_element(By.ID,'onetrust-accept-btn-handler') #ver si el consent button va siempre, creo que no
        consent_button.click()

    except NoSuchElementException:
        time.sleep(4)  # Espera 4 segundos si no aparece, mismo proceso

        try:
            consent_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
            consent_button.click()

        except NoSuchElementException:
            pass

    
    time.sleep(6)
    
    try:
        move_down = driver.find_element(By.CSS_SELECTOR,'.vtex-rich-text-0-x-wrapper.vtex-rich-text-0-x-wrapper--promoInfo')
        ActionChains(driver).move_to_element(move_down).perform()
    except:
        pass

    css_selector_button = '.lyracons-search-result-1-x-paginationButtonChangePage.mr3.flex.justify-center'
    cambio_pagina = driver.find_elements(By.CSS_SELECTOR,css_selector_button)

    time.sleep(8)
    final_work=[] # list where i hold all the data       

    try:
        total=driver.find_element(By.CSS_SELECTOR,'.valtech-carrefourar-search-result-0-x-totalProducts--layout').text
        print(total)
        number = int(total.split()[0])
      
        if number==0: #primera condicion probabemente innecesaria
        
            print(f'{number} and {type(number)}')
            return final_work
        elif number%16==0:
            number_pages= int(number/16) #hay un bug entre la hoja 1 y hoja 2 de productos que genera un error. 
        else:
            number_pages= int(number//16+1)

        print(f'Total number of products: {number}')
        print(f'Total number pages: {number_pages}')

    except NoSuchElementException: #hay casos que no hay ningun elemento
        print("Total products element not found.")
        return final_work
    ######
    time.sleep(5)
    
    elements=driver.find_elements(By.CSS_SELECTOR,'article.vtex-product-summary-2-x-element.vtex-product-summary-2-x-element--contentProduct')
    time.sleep(1)
    source=driver.page_source
    
    
    try:
        print(f'page number: 1')
        final_work.extend(products(source,category,sub))
    except TimeoutException:
        print('Error Loading or no element available')
        return final_work
    except Exception as e:
        print(f'Error: {str(e)}')
        return final_work

    try:
        #time.sleep(4)
        button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[value="2"]')))
    
        print(f'page number: 2') 
        #button= driver.find_element(By.CSS_SELECTOR,'button[value="2"]')
        ActionChains(driver).move_to_element(button).perform()
        time.sleep(8)
        button.click()
        time.sleep(8)
        source= driver.page_source
        final_work.extend(products(source, category, sub))
        time.sleep(1)
    
    except NoSuchElementException:
        print('Error: Element not found')
        return final_work
    except Exception as e:
        print(f'Error: {str(e)}')
        return final_work
        

    if number_pages>2: #cambio el number_page por uno mayor, asi borro

        for i in range(3,number_pages+1):  #loop de paginas
            try:
                #time.sleep(4)
                button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[value="{i}"]')))
                #button= driver.find_element(By.CSS_SELECTOR,f'button[value="{i}"]')
                print(f'page number: {i}')
                ActionChains(driver).move_to_element(button).perform()
                time.sleep(8)
                button.click()
                time.sleep(8)
                source= driver.page_source
                final_work.extend(products(source, category, sub)) #hold the data
                time.sleep(2)
            except:
                break
    else:
        pass

    return final_work



# main_data= pd.read_csv('../csv/carrefour/20230410carrefour_links.csv') #this csv file contains the
#                                                                        #main categories


# full = [full_data(i,u,y) for i,u,y in zip(main_data['links'],main_data['categories'],main_data['subcategories'])]


# df=[]
# for i in full:
#     for x in i:
#         row=pd.DataFrame([x])
#         print(f'this is the dictionary :{x}')
#         df.append(row)
        

# dfs=pd.concat(df) 

# dfs=dfs.reset_index().drop(columns='index') 
# today = date.today() #hold the date
# d1 = today.strftime("%Y%m%d") 
# dfs.to_csv(f'../csv/carrefour/{d1}_carrefour_products.csv', encoding='utf-8', index=False) #always printing the date of the csv file



