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
    PATH = 'C:\Program Files (x86)\chromedriver.exe'

    link = 'https://www.vea.com.ar/'

    s= Service(PATH)

    driver=webdriver.Chrome(service=s)

    driver.maximize_window()

    driver.get(link)
    time.sleep(16)
#cancel button  ----> the web page took off this element
    #driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()

    time.sleep(6) 
    menu_button=driver.find_element(By.CLASS_NAME,'pr9.items-stretch.vtex-flex-layout-0-x-stretchChildrenWidth').click()
    #clicks the left up button to display the menu

    time.sleep(5)
    iframe=driver.find_element(By.CLASS_NAME,'vtex-menu-2-x-submenu--department-menu') #this looks on the menu displayed

    categories = driver.find_elements(By.CSS_SELECTOR,'li.vtex-menu-2-x-menuItem.vtex-menu-2-x-menuItem--menu-item-secondary')
    #this are the categories from the menu
    action=ActionChains(driver)


    links=[]
    for i in range(1,len(categories)-1):
        time.sleep(2)
        categories = driver.find_elements(By.CSS_SELECTOR,'li.vtex-menu-2-x-menuItem.vtex-menu-2-x-menuItem--menu-item-secondary')
        time.sleep(7)
        action.move_to_element(categories[i]).perform()
        time.sleep(2)
        action.click(categories[i]).perform()
        time.sleep(1)
        url= driver.current_url
        links.append(url)
        time.sleep(6)
        
        menu_button=driver.find_element(By.CLASS_NAME,'pr9.items-stretch.vtex-flex-layout-0-x-stretchChildrenWidth')
        time.sleep(3)
        menu_button.click()

    driver.quit()

    return links


###############################################################################################

#this funcs gives the view all to analyze

def urls_analyze(link):

    links=link

    PATH = 'C:\Program Files (x86)\chromedriver.exe'



    s= Service(PATH)

    driver=webdriver.Chrome(service=s)

    driver.maximize_window()

    driver.get(links)
    time.sleep(15)


#cancel button --->the same as before, the web page has no longer this button
    #driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,'div.categoryList-box')
    driver.implicitly_wait(2)
    driver.find_element(By.CSS_SELECTOR,'a.categoryList__viewAll').click()

    driver.quit()

    return driver.current_url

############################################################################################

#gives all pages and categories
def all_pages(link):

    PATH = 'C:\Program Files (x86)\chromedriver.exe'

    links= link

    s= Service(PATH)

    driver=webdriver.Chrome(service=s)

    driver.maximize_window()

    driver.get(links)
    time.sleep(15)

#cancel button -->no longer this button
    #driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()
    time.sleep(3)
    html=driver.page_source

    soup=BeautifulSoup(html,'html.parser')

    category= soup.find('h1',{'class':'vtex-search-result-3-x-galleryTitle--layout t-heading-1'}).text
    print(category)

#full element
    elem= soup.find('div',{'class':'vtex-search-result-3-x-totalProducts--layout pv5 ph9 bn-ns bt-s b--muted-5 tc-s tl t-action--small'}).span.text
#selecting the first value
    number=elem.split()[0]

    
    if int(number)%20 ==0:  #Every page has got 20 products in its link. And we have the full number of products.
        number_page=int(int(number)/20)    # So we can have got the number page
    else:
        number_page= int(int(number)//20 +1) 

    print(f'number of products: {number}')
    print(f'number of pages: {number_page}')

    #number of categories
    category_list_page= [category]*number_page
    total_link= [f'{links}&page={i}' for i in range(1,number_page+1)]
    
    #if len(category_list_page)<50:
    #    del category_list_page[and len(total_link)<50:


    
    return total_link, category_list_page


################################################################################################


#Take the data from each product
def products(link,category):
    
    PATH = 'C:\Program Files (x86)\chromedriver.exe'

    links= link
    categoria=category
    s= Service(PATH)

    driver=webdriver.Chrome(service=s)

    driver.maximize_window()

    driver.get(links)
    time.sleep(15)

#cancel button --> No longer this button
    #driver.find_element(By.ID,'onesignal-slidedown-cancel-button').click()
    #time.sleep(8)
    
    
    go_down=driver.find_element(By.CSS_SELECTOR,'.vtex-search-result-3-x-buttonShowMore.vtex-search-result-3-x-buttonShowMore--fetch-more-hs.w-100.flex.justify-center')
    time.sleep(3)
    ActionChains(driver).move_to_element(go_down).perform()
    time.sleep(3)
    html=driver.page_source
    time.sleep(5)
    soup=BeautifulSoup(html,'html.parser')

    products= soup.find_all('article',class_='vtex-product-summary-2-x-element pointer pt3 pb4 flex flex-column h-100')

    

    current_product= {'Supermercado':'Vea','Categoría': categoria}
    cont=0
    for prod in products:
        cont+=1
        print(f'scrap product: {cont}/{len(products)}')
        
        brand=prod.find('span',class_='vtex-product-summary-2-x-productBrandName').text
        print(brand)
        description = prod.find('span',class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body').text
        print(description)
        
        try:
            block= prod.find('div',class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--mainRow-price-box')
            sub_block=block.find('div',class_='vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--sellingPrice-discount')
            sub_sub_block = sub_block.find('span',class_='veaargentina-store-theme-1vId-Z5l1K6K82ho-1PHy6').text
            print(block)
            print(sub_block)
            print(sub_sub_block)
        except AttributeError:
            print('no hay')
        
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
        
        current_product['brand'] = brand
        current_product['description'] = description
        
        

        current_product['imagen']= prod_img
    driver.quit()    

    return current_product


#############################################################################
section_links= get_urls() #first func
getting_urls=[urls_analyze(i) for i in section_links] #second func 
full_links=[all_pages(i) for i in getting_urls if len(all_pages(i)[0]) <50 ] #third func
                                                                            #the if statement is needed because we have
                                                                             #some problem when we have more than 50 pages
                                                                             #for element. This isn't finished

data=[] #Store the product list here

for num in range(0,13):             #4th func--> [0] and [1] is because
    for i,u in zip(full_links[num][0],full_links[num][1]):


        store= products(i,u)
        data.append(store)

df_products = pd.DataFrame(data) #create the dataframe
today = date.today() #hold the date
d1 = today.strftime("%Y%m%d") 
df_products.to_csv(f'../csv/{d1}_vea_products.csv', encoding='utf-8', index=False) #always printing the date of the csv file