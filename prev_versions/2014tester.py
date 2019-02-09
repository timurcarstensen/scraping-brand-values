from bs4 import BeautifulSoup as soup
import csv
from urllib.request import urlopen as uReq
import pandas as pd
import all_functions

uClient = uReq('https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=866')  # downloading the website
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, 'lxml')

brandNames = []
brandValues = []

for brand_item in page_soup.findAll('div', class_='name'):
    for name in brand_item.findAll('a'):
        i = name.text.strip()
        brandNames.append(i)

for valuation in page_soup.findAll('div', class_='weighted'):
    i = valuation.text.strip()
    brandValues.append(i)

print(brandNames)
print(brandValues)
