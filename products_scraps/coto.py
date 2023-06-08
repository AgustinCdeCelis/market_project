import pandas as pd
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
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException
from datetime import date


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
    


#this function takes the product's data
def take_product(categorias,url):



    r = requests.get(url)


    soup =BeautifulSoup(r.text,'html.parser')

    products = soup.find_all('li',class_='clearfix')

    
    count_product=0
    product_list=[]
    for product_description in products:

        #contador
        count_product=count_product+1
        #this is the count fraction to check the scrapped elements
        print(f'categoria : {categorias}')
        print(f'{count_product} / {len(products)} Elemento escrapeado')

        current_product={'market':'Coto','category': categorias,
                         'currency':'ARG'}
        time.sleep(1)

        #link product
        #link_product=product_description.find('a')['href'] #lo mando abajo
        
        #current_product['link_pagina'] = link_product
        #description product
        description= product_description.find('div',class_='descrip_full').text
        #description_product.append(description)
        current_product['descripcion'] = description

        #precio por unidad
        try:
            unidad = product_description.find('div',class_='price_regular_container').text
            #precio_contado.append(unidad)
            current_product['precio'] = unidad
        except AttributeError:
            unidad = product_description.find('span',class_='atg_store_newPrice').text
            #precio_contado.append(unidad)
            current_product['precio'] = unidad


        #descuento
        try:
            descuento = product_description.find('span',class_='text_price_discount').text
            print(descuento)
            #promocion.append(descuento)
            current_product['descuento'] =descuento
        except AttributeError:
            #promocion.append(None)
            current_product['descuento'] =None

        #precio descuento
        try:
            precio_final=product_description.find('span',class_='price_discount').text
            print(precio_final)
            #precio_descuento.append(precio_final)
            current_product['precio_descuento'] = precio_final
        except AttributeError:
            #precio_descuento.append(None)
            current_product['precio_descuento'] = None

        link_product=product_description.find('a')['href'] 
        current_product['link_pagina'] = link_product #mande abajo

        try:
            precio_unidad = product_description.find('span',class_='unit').text
            current_product['precio_unidad'] =precio_unidad
        except:
            current_product['precio_unidad'] = None     

        product_list.append(current_product)

    return product_list


#full data
def full_urls(partial_link,names_categories):
    #PATH= 'C:\Program Files (x86)\chromedriver.exe'
    PATH= "/usr/lib/chromium-browser/chromedriver"

    link_total = 'https://www.cotodigital3.com.ar'+partial_link

    s = Service(PATH)

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Habilitar el modo sin cabeza
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options,service=s)
    #driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    
    time.sleep(8)
    driver.get(link_total)
    time.sleep(1)
    driver.maximize_window()
    time.sleep(2)
    

    cont=1
    print(f'cantidad hojas {cont}')
    final_work=[] # list where i hold all the data
    data= take_product(names_categories,link_total)
    
    final_work.extend(data)


    while True:
            try:
                next = driver.find_element(By.LINK_TEXT,'Sig')
                time.sleep(2)
                next.click()
                pages= driver.current_url
                cont+=1
                print(f'cantidad hojas {cont}')
                data = take_product(names_categories,pages)
                
                final_work.extend(data)
                #total_urls.append(pages)
                
                time.sleep(4)
            except:
                 break
                 
                 
    sig= driver.find_elements(By.CSS_SELECTOR,'a[title*="Ir a página"]')
    
    for i in range(1,len(sig)):
        try:
            sig= driver.find_elements(By.CSS_SELECTOR,'a[title*="Ir a página"]')
            time.sleep(2)
            sig[i].click()
            cont+=1
            print(f'cantidad hojas {cont}')
            pages= driver.current_url
            data = take_product(names_categories,pages)
            
            final_work.extend(data)
            #total_urls.append(pages)
            time.sleep(4)
        except IndexError:
            sig = driver.find_elements(By.CSS_SELECTOR,'a[title*="Ir a página"]')
            time.sleep(2)
            sig[1].click()
            cont+=1
            print(f'cantidad hojas {cont}')
            pages=driver.current_url
            data = take_product(names_categories,pages)
            
            final_work.extend(data)
            #total_urls.append(pages)
            time.sleep(4)
    
    
    

    driver.quit()

    print(f' the len of final_work is {len(final_work)}')

    df = pd.DataFrame(final_work)

    return df



# #this variable holds the function of categories and first links. This links have to iterate to another pages
# first_step = take_url()



# #2 loop every category to take the data
# main_data=[]
# for link,title in zip(first_step[0],first_step[1]):
#     try:
        
#         data1=full_urls(link,title)
#         main_data.append(data1)
#     except:
#         print('#######################################################################')
#         print("--------------------------NO SCRAPEO-----------------------------------")
#         print('#######################################################################')
#         pass


# df=pd.concat(main_data)
# df['precio'] =df['precio'].str.replace('\t','').str.replace('\n','')
# df['precio_unidad'] =df['precio_unidad'].str.replace('\t','').str.replace('\n','').str.replace('  ','')

# df =df.drop_duplicates()
# df = df.reset_index().drop(columns='index') 

# today = date.today()
# d1 = today.strftime("%Y%m%d")

# df.to_csv(f'../csv/coto/{d1}_coto_products.csv', encoding='utf-8', index=False)





