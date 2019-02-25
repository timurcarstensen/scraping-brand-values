# DEVELOP

import functions as fnc
from bs4 import BeautifulSoup
import pandas as pd

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}


def getUrlDictInterbrand(url: str) -> dict:
    d = dict()

    rng = range(2000, 2019)
    for i in rng:
        s = url[:58] + str(i) + url[62:]
        d[i] = s

    return d


def returnDataFrameInterbrand(url: str, hdr: dict, currentYear: int):  # scrapes data off website and returns dataframe with the values
    
    p = soup(fnc.downloadWebsite(url, hdr), 'lxml')  # using the downloadWebsite function to download the website

    names = []
    values = []
    sources = []
    years = []

    source = p.find('div', class_='col-50 left copyright-year text-tiny').text.strip()[7:17]  # finds the current source

    for b in p.findAll('li', class_='brand-item'):  # loop over all brands and collect name and brand value
        for n in b.find('div', class_='brand-info brand-name brand-col-4'):
            names.append(n.strip())

        for z in b.find('div', class_='brand-info brand-value brand-col-7'):
            values.append(z.strip())

    for i in names:  # adding as many sources (in this case just Interbrand as this is the interbrand function) and the currentYear into a list
        sources.append(source)
        years.append(currentYear)

    brand_tuples = list(zip(names, values, sources, years))  # using all the lists to create tuples with 4 arguments

    df = pd.DataFrame(brand_tuples, columns=['name', 'value', 'source', 'year'])  # using the tuple which we created above to create a dataframe

    # print(df)

    return df


# TESTING CODE

dictionary = getUrlDictInterbrand('https://www.interbrand.com/best-brands/best-global-brands/2018/ranking/')

for x, y in dictionary.items():
    returnDataFrameInterbrand(y, headers, x)
    

