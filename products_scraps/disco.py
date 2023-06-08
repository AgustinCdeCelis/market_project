import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
#time
import time
from selenium.webdriver.chrome.options import Options
import re
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
from unidecode import unidecode



#looking at the dataframe

#df = pd.read_csv('./csv/disco/20230427disco_links.csv')

##################################################################
#------------------------first part-------------------------------
##################################################################


#gives all pages and categories that has less than 50 elements

#CODIGO PRINCIPAL
def all_pages(category,link):

    #PATH = 'C:\Program Files (x86)\chromedriver.exe'
    PATH = '/usr/lib/chromium-browser/chromedriver'

    links= link

    s= Service(PATH)

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Habilitar el modo sin cabeza
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver=webdriver.Chrome(service=s,options=chrome_options)

    driver.maximize_window()

    driver.get(links)
    time.sleep(15)

#cancel button
    #driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()
    time.sleep(3)
    html=driver.page_source

    soup=BeautifulSoup(html,'html.parser')

    #category= soup.find('h1',{'class':'vtex-search-result-3-x-galleryTitle--layout t-heading-1'}).text
    print(category)

#full element
    elem= soup.find('div',{'class':'vtex-search-result-3-x-totalProducts--layout pv5 ph9 bn-ns bt-s b--muted-5 tc-s tl t-action--small'}).span.text
#selecting the first value
    number=elem.split()[0] #number contains

    
    if int(number)%20 ==0: #to know how many pages got 
        number_page=int(int(number)/20)
    else:
        number_page= int(int(number)//20 +1) 

    print(f'number of products: {number}')
    print(f'number of pages: {number_page}')

    #number of categories
    category_list_page= [category]*number_page
    total_link= [f'{links}&page={i}' for i in range(1,number_page+1)]
    
    

    driver.quit()
    
    return total_link, category_list_page



# full_links=[] #dividing into more than 50 and less
# other = []
# for i,u in zip(df['categorias'],df['links']):
#     links, category_list = all_pages(i, u)
#     data = (links, category_list)
#     if len(links) <= 50: #50 links x 20 elements
#         full_links.append(data)
#     else:
#         other.append([u, i]) #other contains the categories with more than 1000 elements
    


############################################################################################3
#----------------------------PRINCIPAL CODE PART--------------------------------------------
############################################################################################

#codigo principal




def products(link,category):
    
    PATH = '/usr/lib/chromium-browser/chromedriver'

    links= link
    categoria=category
    s= Service(PATH)

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Habilitar el modo sin cabeza
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver=webdriver.Chrome(service=s,options=chrome_options)

    driver.maximize_window()

    driver.get(links)
    time.sleep(15)

#cancel button
    #driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()
    #time.sleep(8)
    
   #go down to see the whole page ----> the showmorebutton at the end
    go_down=driver.find_element(By.CSS_SELECTOR,'.vtex-search-result-3-x-buttonShowMore.vtex-search-result-3-x-buttonShowMore--fetch-more-hs.w-100.flex.justify-center')
    time.sleep(3)
    ActionChains(driver).move_to_element(go_down).perform()
    time.sleep(3)
    html=driver.page_source
    time.sleep(5)
    soup=BeautifulSoup(html,'html.parser')

    products= soup.find_all('article',class_='vtex-product-summary-2-x-element pointer pt3 pb4 flex flex-column h-100')

    

    
    cont=0
    p=[]
    for prod in products:
        cont+=1
        current_product= {'Supermercado':'disco','Categoría': categoria}
        print(f'scrap product: {cont}/{len(products)}')
        try:
            brand=prod.find('span',class_='vtex-product-summary-2-x-productBrandName').text
            print(brand)
        except:
            pass
        description = prod.find('span',class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body').text
        print(description)
        
        #promo=prod.find('div',class_= 'vtex-flex-layout-0-x-stretchChildrenWidth')
        ##########
        try:
            block= prod.find('div',class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--mainRow-price-box')
            sub_block=block.find('div',class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--sellingPrice-discount')
            sub_sub_block = sub_block.find('span',class_='veaargentina-store-theme-1vId-Z5l1K6K82ho-1PHy6').text
            print(block)
            print(sub_block)
            print(sub_sub_block)
        except AttributeError:
            print('no hay')




        #########################################
        
        prod_img = prod.find('img').get('src')
        print(prod_img)
        full_price = prod.find('div',class_='contenedor-precio').text
        print(full_price)
        if full_price.count('$')==2:
            descuento=full_price.split('$',2)[1]
            precio=full_price.split('$',2)[2]
            current_product['precio'] = f'${precio}'
            current_product['descuento']=f'${descuento}'
        else:

            current_product['precio'] = full_price
            current_product['descuento'] = None
        print('#######################################################################################')
        try:
            current_product['brand'] = brand
        except:
            current_product['brand'] = None
        current_product['description'] = description
        #current_product['promocion'] = promo
        

        current_product['imagen']= prod_img
        p.append(current_product)
    driver.quit()    

    df= pd.DataFrame(p)

    return df


# data=[] #el numero de variables puede variar

# for num in range(len(full_links)):
#     for i,u in zip(full_links[num][0],full_links[num][1]):


#         store= products(i,u)
#         data.append(store)


# df_products1 =pd.concat(data) #first DF with DF LESS THAN 1000 PRODUCTS

# df_products1 =df_products1.drop_duplicates()



######################################################################################
#-----------------------------EXCEPT PART--------------------------------------------
######################################################################################

#This part takes the links and categories that got the links with more than 1000 product


def exception(links): #funcion que da el largo de subcategorias en casos con mas de 50 links

    PATH = '/usr/lib/chromium-browser/chromedriver'

    s= Service(PATH)

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Habilitar el modo sin cabeza
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver=webdriver.Chrome(service=s,options=chrome_options)

    driver.maximize_window()

    driver.get(links)
    time.sleep(16)

    #cancel button
    try:
        driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()
    except:
        pass
    time.sleep(3)

    bar = driver.find_element(By.CSS_SELECTOR,'div.vtex-search-result-3-x-filterTemplateOverflow.pb5.overflow-y-auto')
    

    #ver si esto va
    subcat_title = driver.find_elements(By.CSS_SELECTOR, '.vtex-search-result-3-x-filterTitleSpan')
    #print(len(subcat_title))
    for i in subcat_title:
        #print(i.text)
        if i.text == 'Sub-Categoría':  #busco la subcategoria para que pueda clickear bien el item
                 
            driver.execute_script("arguments[0].scrollIntoView();", i)
    time.sleep(2)
    
    go_down= driver.find_element(By.CSS_SELECTOR,'.vtex-search-result-3-x-buttonShowMore--layout') #voy abajo para que detecte bien el link
    ActionChains(driver).move_to_element(go_down).perform()
    time.sleep(5)
    #tag= driver.find_elements(By.CSS_SELECTOR,'button.vtex-search-result-3-x-seeMoreButton.mt2.pv2.bn.pointer.c-link')
    tag= driver.find_elements(By.CSS_SELECTOR,'.vtex-search-result-3-x-seeMoreButton.mt2.pv2.bn.pointer.c-link')
    #print(f' la longitud de los tags {len(tag)}')

    
    ActionChains(driver).move_to_element(tag[2]).click().perform() #el tag que hay que desplegar es el 2
    
    
    time.sleep(2)


    sub=driver.find_elements(By.CSS_SELECTOR,'label[for*="category-3"]')
    #print(f' cantidad de subcategorias: {len(sub)}')
    #driver.close()


    time.sleep(3)
    
    
    print(len(sub))
    return len(sub)





def products_except(link,category): #funcion que da la cantidad de productos
    
    
    soup=BeautifulSoup(link)

    products= soup.find_all('article',class_='vtex-product-summary-2-x-element pointer pt3 pb4 flex flex-column h-100')

    
    cont=0

    p=[]
    for prod in products:
        cont+=1
        print(f'scrap product: {cont}/{len(products)}') #looking at scrap product
        #define the list of each produc
        current_product= {'Supermercado':'Disco','Categoría': category}
        
        brand=prod.find('span',class_='vtex-product-summary-2-x-productBrandName').text
        #print(brand)
        description = prod.find('span',class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body').text
        #print(description)
        
        #promo=prod.find('div',class_= 'vtex-flex-layout-0-x-stretchChildrenWidth')
        ##########
        # try:
        #     block= prod.find('div',class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--mainRow-price-box')
        #     sub_block=block.find('div',class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--sellingPrice-discount')
        #     sub_sub_block = sub_block.find('span',class_='veaargentina-store-theme-1vId-Z5l1K6K82ho-1PHy6').text
        #     #print(block)
        #     #print(sub_block)
        #     #print(sub_sub_block)
        # except AttributeError:
        #     #print('no hay')
            

        #########################################
        
        prod_img = prod.find('img').get('src')
        #print(prod_img)
        full_price = prod.find('div',class_='contenedor-precio').text
        #print(full_price)
        if full_price.count('$')==2:
            descuento=full_price.split('$',2)[1]
            precio=full_price.split('$',2)[2]
            current_product['precio'] = f'${precio}'
            current_product['descuento']=f'${descuento}'
        else:

            current_product['precio'] = full_price
            current_product['descuento'] = None
        #print('#######################################################################################')
        
        current_product['brand'] = brand
        current_product['description'] = description
        #current_product['promocion'] = promo
        

        current_product['imagen']= prod_img
        print(current_product)
        p.append(current_product)
        print('#######################################################################################')


        
    return p





def total(links,categoria): #funcion que da el total de categorias y productos

    first_part=exception(links) #take links

    


    data=[]
    cont=0
    
    for num_category in range(first_part):   #saque categories                     
        
        PATH = '/usr/lib/chromium-browser/chromedriver' ### achieve link part

        s= Service(PATH)

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Habilitar el modo sin cabeza
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver=webdriver.Chrome(service=s,options=chrome_options)

        driver.maximize_window()

        driver.get(links)
        time.sleep(16)

    #cancel button
        try:
            driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()
        except:
            pass
        time.sleep(3)

        bar = driver.find_element(By.CSS_SELECTOR,'div.vtex-search-result-3-x-filterTemplateOverflow.pb5.overflow-y-auto')

        subcat_title = driver.find_elements(By.CSS_SELECTOR, '.vtex-search-result-3-x-filterTitleSpan')
        
        for i in subcat_title: 
            #print(i.text)
            if i.text == 'Sub-Categoría':  #busco la subcategoria para que pueda clickear bien el item
                 
                driver.execute_script("arguments[0].scrollIntoView();", i)
            time.sleep(2)

        go_down= driver.find_element(By.CSS_SELECTOR,'.vtex-search-result-3-x-buttonShowMore--layout') #voy abajo para que detecte bien el link
        ActionChains(driver).move_to_element(go_down).perform() 
        time.sleep(5)

        #more button
        tag= driver.find_elements(By.CSS_SELECTOR,'button.vtex-search-result-3-x-seeMoreButton.mt2.pv2.bn.pointer.c-link')[2]

        ActionChains(driver).move_to_element(tag).click().perform()


        time.sleep(2)
    
        #the subcategories elements
        sub=driver.find_elements(By.CSS_SELECTOR,'label[for*="category-3"]')
        
        #the sub-category title
        elemento =driver.find_elements(By.CSS_SELECTOR,'.vtex-search-result-3-x-filterTitleSpan')[2]
        print(sub[num_category].text)
     

        ActionChains(driver).move_to_element(elemento).perform()
        time.sleep(1)
        ActionChains(driver).move_to_element(sub[num_category]).perform()
        sub[num_category].click()
        time.sleep(4)


        cont+=1
        print(f'esta es la categoria n°: {cont}')
    
   

        time.sleep(5)
        loops=0

        while True:
        
            try:   
                loops+=1
                #try:
                #problemas con el codigo cuando tengo a partir del 50 loop
                print(f'number of loops: {loops}')
           #selector de ir abajo
                go_down=driver.find_element(By.CSS_SELECTOR,'.vtex-search-result-3-x-buttonShowMore--layout')
                        #go_down=driver.find_element(By.CSS_SELECTOR,'.vtex-search-result-3-x-buttonShowMore.vtex-search-result-3-x-buttonShowMore--fetch-more-hs.w-100.flex.justify-center')
        
                ActionChains(driver).move_to_element(go_down).perform() #va abajo
                time.sleep(3)
                go_up =driver.find_element(By.CSS_SELECTOR,'div.vtex-search-result-3-x-totalProducts--layout')
                ActionChains(driver).move_to_element(go_up).perform()
                time.sleep(2)
                ActionChains(driver).move_to_element(go_down).perform() #va abajo
                time.sleep(3)
                data2=products_except(driver.page_source,categoria) #saco los datos
                data.extend(data2) 
           
                time.sleep(7)
        #
                button=driver.find_element(By.CSS_SELECTOR,'.vtex-search-result-3-x-buttonShowMore.vtex-search-result-3-x-buttonShowMore--fetch-more-hs.w-100.flex.justify-center')
            
                button.click()
                time.sleep(5)
                
            except:
                break 
             
        driver.quit()
        time.sleep(3)
    
    df=pd.DataFrame(data)
    return df


# info= [total(i,u) for i,u in other]

# df =pd.concat(info)  #df with more than 1000 elements

# df =df.drop_duplicates()


# definite_df =pd.concat([df,df_products1])




# definite_df = definite_df.reset_index().drop(columns='index') 

# today = date.today()
# d1 = today.strftime("%Y%m%d")

# definite_df.to_csv(f'./csv/disco/{d1}_disco_products.csv', encoding='utf-8', index=False)
        
