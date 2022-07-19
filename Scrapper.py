#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib3
import pandas as pd

from elasticsearch import Elasticsearch
host = 'https://localhost:9200'
user = 'elastic'
password = 'eSoWEgYDQVDYfS3TZ0BH'
es = Elasticsearch(host
                   ,ca_certs=False
                   ,verify_certs=False
                   ,basic_auth=('elastic','eSoWEgYDQVDYfS3TZ0BH')
                   )
    
def SearchItem(driverPath, url, product):
    #SETANDO OPCOES DO NAVEGADOR
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    
    #APLICANDO AS CONFIGURACOES NO NAVEGADOR
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path = driverPath)
    #BUSCA A URL SOLICITADA
    driver.get(url)
    
    #EFETUA A BUSCA NO NAVEGADOR
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(product)
    search_box.submit()
    
    #PEGA OS ITENS QUE CONTEM sh-dgr__content NO NOME DA CLASSE
    itemList = driver.find_elements(By.CLASS_NAME, 'sh-dgr__content')
    
    #CRIA LISTAS VAZIAS PARA NOME, PRECO E LOJA DO ITEM VENDIDO
    itemName = []
    itemPrice = []
    itemStore = []
    
    #COLOCA ESSAS INFORMACOES NAS LISTAS
    for item in itemList:
        contentBox = item.text.splitlines()
        itemName.append(contentBox[0])
        
        if len(contentBox) == 4 or len(contentBox) == 5:
            itemPrice.append(contentBox[1])
            itemStore.append(contentBox[2])
            
        if len(contentBox) == 6 or len(contentBox) == 7:
            itemPrice.append(contentBox[3])
            itemStore.append(contentBox[4])
            
        elif len(contentBox) == 8:
            itemPrice.append(contentBox[4])
            itemStore.append(contentBox[5])
    
    # res = es.indices.analyze({
    #       "analyzer" : "keyword",
    #       "text" : product
    #     })
    
    res = es.indices.analyze(tokenizer='keyword'
                             ,text=product                             
                             ,filter=("lowercase", "asciifolding"))
    
    for i in res['tokens']:
        print(i['token'])
    print("\n")
    
    # df = pd.DataFrame(itemPrice, index = itemName, columns=['Price'])
    # df['Store'] = itemStore
    # print(df.head(10))
    
#----------------------------CHAMADAS DE FUNÇÕES------------------------------#

driverPath = '/home/gustavooguto/UTFPR/Scrapper/chromedriver'
url = 'https://shopping.google.com/'
product = 'Papel Sulfite A4 Chamex 75g 500 folhas'

urllib3.disable_warnings()
SearchItem(driverPath, url, product)