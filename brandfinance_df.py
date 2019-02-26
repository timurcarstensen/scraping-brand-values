# DEVELOP
from bs4 import BeautifulSoup as soup
import pandas as pd
import functions as fnc


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}

brandfinance_url = 'https://brandirectory.com/league_tables/table/global-500-2018'


def returnUrlDictBrandDirectory(url: str) -> dict:  # takes in a initial url and retuns a dictionary (Year : Corresponding link)
    u_dict = dict()
    link = url[:(len(url) - 4)]

    for i in range(2007, 2019):
        if i == 2007:  # adding exception for the year 2007 as the link format is slightly different
            z = 'https://brandirectory.com/league_tables/table/global-250-2007'
            u_dict[i] = z
        else:
            x = url[:(len(url) - 4)] + str(i)
            u_dict[i] = x

    return u_dict


def returnDataFrameBrandDirectory(url: str, hdr: dict):  # takes a link (string) and a header (dictionary) and returns a dataframe

    p = soup(fnc.downloadWebsite(url, hdr), 'lxml')

    y = int(url[-4:])
    s = 'BrandFinance'

    names = list()
    values = list()
    sources = list()
    years = list()

    for x in p.findAll('td', class_='leftalign table_name'):
        for i in x.find('a'):
            if len(names) <= 99:
                names.append(i)

    for v in p.findAll('td', class_='c v1'):
        for i in v.findAll('span', class_='o'):
            values.append(i.text.replace(',', ''))

    for i in names:
        sources.append(s)
        years.append(y)

    tuples = list(zip(names, values, sources, years))

    df = pd.DataFrame(tuples, columns=['NAME', 'VALUE', 'SOURCE', 'YEAR'])

    print('done with ' + str(y) + '!')

    return df


def concatDataFramesWriteCsvBrandFinance(url: str, headers: dict, outputName: str):
    l = list()

    for x, y in returnUrlDictBrandDirectory(url).items():
        l.append(returnDataFrameBrandDirectory(y, headers))

    f = pd.concat(l)
    f.to_csv(outputName, index=False, header=False)
