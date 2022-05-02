import requests 
from bs4 import BeautifulSoup 
import pandas as pd
import json

quote_list = []
author_firstname_list = ['Elon','Jeff','Bernard','Bill','Gautam','Warren','Mukesh','Larry','Larry','Sergey']
author_surname_list = ['Musk','Bezos','Arnault','Gates','Adani','Buffett','Ambani','Ellison','Page','Brin']
last_page_list = [4, 2, 1, 7, 1, 2, 1, 1, 1, 1]

def get_quotes(author_firstname, author_surname, first_page, last_page):
    author_fullname = author_firstname+'_'+author_surname
    for page in range(first_page,last_page+1):
        print(f'-------------------page:{page}---------------------------')
        print(author_fullname)
        URL = f"https://www.brainyquote.com/authors/{author_firstname}-{author_surname}-quotes_{page}"
        r = requests.get(URL) 

        soup = BeautifulSoup(r.content, 'html.parser') 
        #print(soup.prettify()) 

        divs = soup.find_all('div', attrs={'style': 'display: flex;justify-content: space-between'})
        num_of_quotes = len(divs)
        print(f'number of quotes: {num_of_quotes}')

        for div in divs:
            quo_text = div.text.strip()
            quote_list.append({'quote':quo_text,'author':author_fullname})
    
    with open(f"/Users/emma/Desktop/Python_Projects/QuotesAPI/top_10_billionairs_quotes_1.json", 'w') as f:
        json.dump(quote_list, f)
        print('JSON exported!')
    

for first, last, last_page in zip(author_firstname_list, author_surname_list, last_page_list):
    get_quotes(first,last,1,last_page)