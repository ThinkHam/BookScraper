from asyncio.windows_events import NULL
import requests
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from scipy import stats
from re import sub

products = {}

#url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw={keyword}&_sacat=0&_pgn={pagenum}'
url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw={keyword}&_sacat=0&_ipg=240&_pgn={pagenum}&rt=nc&LH_BIN=1'
test_keyword = 'ultrasound+textbook'

def main():
    
    #Scraping
    for i in range(1,2):
        request = requests.get(url.format(keyword = test_keyword, pagenum = i))
        data = request.text
        soup = bs(data)
        listings = soup.find_all('li', attrs={'class': 's-item'})
        for listing in listings:
            product_name = ''
            product_price = ''
            for name in listing.find_all('h3', attrs={'class':'s-item__title'}):
                if str(name.find(text=True, recursive=False))!='None':
                    product_name = str(name.find(text=True, recursive=False))
                    products[product_name] = 0
            if product_name!='':
                price = listing.find('span', attrs={'class':'s-item__price'})
                product_price = str(price.find(text=True, recursive=False))
                try:
                    product_price = float(product_price[1:])
                    if products[product_name] == 0:
                        products[product_name] = product_price
                except ValueError:
                    continue
                        
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump({key: val for key, val in sorted(products.items(), key = lambda ele: ele[1])}, f, ensure_ascii=False, indent=4)
                
    
    #Formatting
    
    
if __name__ == '__main__':
    main()