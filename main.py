from links import dia_links,disco_links,jumbo_links,vea_links,carrefour_links, set_csv
from datetime import date
from products_scraps import coto, dia_products, carrefour_products, jumbo, vea, disco

from products_scraps.vea import exception,products_except
from products_scraps.disco import exception,products_except
from products_scraps.jumbo import exception,products_except
import pandas as pd

set_csv.export_links_to_csv(dia_links.full(), 'dia')
#set_csv.export_links_to_csv(disco_links.get_urls(), 'disco')
#set_csv.export_links_to_csv(jumbo_links.get_urls(), 'jumbo')
#set_csv.export_links_to_csv(vea_links.get_urls(), 'vea')
#set_csv.export_links_to_csv(carrefour_links.info(), 'carrefour')


################################################################################

#DIA

today = date.today()
d1 = today.strftime("%Y%m%d")

main_data= pd.read_csv(f'./csv/dia/{d1}dia_links.csv') #loading the csv from files

main_data= main_data.loc[1:] #take out the promo because there is another web format

#all data
main=[dia_products.full_scrap(i,u) for i,u in zip(main_data['categoria'],main_data['links'])]

dfs=[pd.DataFrame(i) for i in main] # creating the dataframes from each category
df=pd.concat(dfs) #full df

today = date.today()
d1 = today.strftime("%Y%m%d")
df.to_csv(f'./csv/dia/{d1}_dia_products.csv', encoding='utf-8', index=False)


####################################################################################

#CARREFOUR

main_data= pd.read_csv(f'./csv/carrefour/{d1}carrefour_links.csv') #this csv file contains the
                                                                       #main categories


full = [carrefour_products.full_data(i,u,y) for i,u,y in zip(main_data['links'],main_data['categories'],main_data['subcategories'])]


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
dfs.to_csv(f'./csv/carrefour/{d1}_carrefour_products.csv', encoding='utf-8', index=False) #always printing the date of the csv file

######################################################################################

#VEA

df = pd.read_csv(f'./csv/vea/2{d1}vea_links.csv')

full_links=[] #dividing into more than 50 and less
other = []
for i,u in zip(df['categorias'],df['links']):
    links, category_list = vea.all_pages(i, u)
    data = (links, category_list)
    if len(links) <= 50: #50 links x 20 elements
        full_links.append(data)
    else:
        other.append([u, i]) #other contains the categories with more than 1000 elements

####main

data=[] #el numero de variables puede variar

for num in range(len(full_links)):
    for i,u in zip(full_links[num][0],full_links[num][1]):


        store= vea.products(i,u)
        data.append(store)


df_products1 =pd.concat(data) #first DF with DF LESS THAN 1000 PRODUCTS

df_products1 =df_products1.drop_duplicates()

###except

info= [vea.total(i,u) for i,u in other]

df =pd.concat(info)  #df with more than 1000 elements

df =df.drop_duplicates()


definite_df =pd.concat([df,df_products1])




definite_df = definite_df.reset_index().drop(columns='index') 

today = date.today()
d1 = today.strftime("%Y%m%d")

definite_df.to_csv(f'./csv/vea/{d1}_vea_products.csv', encoding='utf-8', index=False)
        

###################################################################################

#DISCO

df = pd.read_csv('./csv/disco/{d1}disco_links.csv')


full_links=[] #dividing into more than 50 and less
other = []
for i,u in zip(df['categorias'],df['links']):
    links, category_list = disco.all_pages(i, u)
    data = (links, category_list)
    if len(links) <= 50: #50 links x 20 elements
        full_links.append(data)
    else:
        other.append([u, i]) #other contains the categories with more than 1000 elements

###########main


data=[] #el numero de variables puede variar

for num in range(len(full_links)):
    for i,u in zip(full_links[num][0],full_links[num][1]):


        store= disco.products(i,u)
        data.append(store)


df_products1 =pd.concat(data) #first DF with DF LESS THAN 1000 PRODUCTS

df_products1 =df_products1.drop_duplicates()
    
###### exception

info= [disco.total(i,u) for i,u in other]

df =pd.concat(info)  #df with more than 1000 elements

df =df.drop_duplicates()


definite_df =pd.concat([df,df_products1])




definite_df = definite_df.reset_index().drop(columns='index') 

today = date.today()
d1 = today.strftime("%Y%m%d")

definite_df.to_csv(f'./csv/disco/{d1}_disco_products.csv', encoding='utf-8', index=False)
        
##################################################################################

#JUMBO

df= pd.read_csv(f'./csv/jumbo/{d1}jumbo_links.csv')


full_links=[] #dividing into more than 50 and less
other = []
for i,u in zip(df['categorias'],df['links']):
    links, category_list = jumbo.all_pages(i, u)
    data = (links, category_list)
    if len(links) <= 50: #50 links x 20 elements
        full_links.append(data)
    else:
        other.append([u, i])


#####first part

data=[] #el numero de variables puede variar

for num in range(len(full_links)):
    for i,u in zip(full_links[num][0],full_links[num][1]):


        store= jumbo.products(i,u)
        data.append(store)


df_products1 =pd.concat(data) #first DF with DF LESS THAN 1000 PRODUCTS

df_products1 =df_products1.drop_duplicates()


######exception

info= [jumbo.total(i,u) for i,u in other]



df =pd.concat(info)  #df with more than 1000 elements

df =df.drop_duplicates()


definite_df =pd.concat([df,df_products1])




definite_df = definite_df.reset_index().drop(columns='index') 

today = date.today()
d1 = today.strftime("%Y%m%d")

definite_df.to_csv(f'./csv/jumbo/{d1}_jumbo_products.csv', encoding='utf-8', index=False)

######################################################################################

#COTO

#this variable holds the function of categories and first links. This links have to iterate to another pages
first_step = coto.take_url()



#2 loop every category to take the data
main_data=[]
for link,title in zip(first_step[0],first_step[1]):
    try:
        
        data1=coto.full_urls(link,title)
        main_data.append(data1)
    except:
        print('#######################################################################')
        print("--------------------------NO SCRAPEO-----------------------------------")
        print('#######################################################################')
        pass


df=pd.concat(main_data)
df['precio'] =df['precio'].str.replace('\t','').str.replace('\n','')
df['precio_unidad'] =df['precio_unidad'].str.replace('\t','').str.replace('\n','').str.replace('  ','')

df =df.drop_duplicates()
df = df.reset_index().drop(columns='index') 

today = date.today()
d1 = today.strftime("%Y%m%d")

df.to_csv(f'./csv/coto/{d1}_coto_products.csv', encoding='utf-8', index=False)

