import pandas as pd
from bs4 import BeautifulSoup
import requests as r
import re

# Parameters
wiki_url = "https://en.wikipedia.org/wiki/List_of_busiest_container_ports"
chunk_size = 24
csv_output_path = '4_BeautifulSoup/world_top_10_container_ports.csv'

# Functions
def parse_wiki(wiki_url):
    wiki_page_request = r.get(wiki_url)
    wiki_page_text = wiki_page_request.text
    soup = BeautifulSoup(wiki_page_text, 'html.parser')
    return soup

def append_headers(soup):
    headers = []
    tclass = soup('table', {"class":"wikitable sortable"})[0:]

    for temp in tclass:
        for t_temp in temp.find_all('th'):
            column_name = re.sub('\[\d{1,3}\]','',t_temp.text.strip())
            headers.append(column_name)
    return headers

def append_rows(soup):
    rows = []
    tclass = soup('table', {"class":"wikitable sortable"})[0:]
    for temp in tclass:
        for t_temp in temp.find_all('td'):
            row = re.sub('\[\d{1,3}\]','',t_temp.text.strip())
            rows.append(row)
    return rows

def append_chunked_list(rows):
    chunked_list = list()
    for i in range (0, len(rows),chunk_size):
        chunked_list.append(rows[i:i+chunk_size])
    return chunked_list

# Run functions
soup = parse_wiki(wiki_url=wiki_url)
headers = append_headers(soup=soup)
rows = append_rows(soup=soup)
chunked_list = append_chunked_list(rows=rows)

# Create dataframe
df = pd.DataFrame(chunked_list,columns=headers)

# Pivot df
df = df.drop(df.columns[0], axis=1)
df = df.iloc[:10].melt(
    id_vars=["Port","Country/ Region","Region","Location"], 
    var_name="Year", 
    value_name="thousand TEUs")

# Export to CSV
df.to_csv(csv_output_path)
print("Exported CSV")

