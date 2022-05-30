from asyncio.windows_events import NULL
import requests
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from scipy import stats
from re import sub

products = []

#url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw={keyword}&_sacat=0&_pgn={pagenum}'
url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw={keyword}&_sacat=0&_ipg=240&_pgn={pagenum}&rt=nc&LH_BIN=1'
test_keyword = 'jumbo+pikachu+yoda+plush'

def main():
    
    #Scraping
    for i in range(1,10):
        request = requests.get(url.format(keyword = test_keyword, pagenum = i))
        data = request.text
        soup = bs(data)
        listings = soup.find_all('li', attrs={'class': 's-item'})
        for listing in listings:
            product_name = ''
            product_price = ''
            product_link = ''
            for name in listing.find_all('h3', attrs={'class':'s-item__title'}):
                if str(name.find(text=True, recursive=False))!='None':
                    product_name = str(name.find(text=True, recursive=False))
            if product_name!='':
                price = listing.find('span', attrs={'class':'s-item__price'})
                product_price = str(price.find(text=True, recursive=False))
                for a in listing.find_all('a', href=True, attrs={'class':'s-item__link'}):
                    product_link = a['href']
                try:
                    product_price = float(product_price[1:])
                    products.append({
                        'Name' : product_name,
                        'Price' : product_price,
                        'Link' : product_link
                    })
                except ValueError:
                    continue
                        
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
                
    
    #Formatting
    
    
if __name__ == '__main__':
    main()