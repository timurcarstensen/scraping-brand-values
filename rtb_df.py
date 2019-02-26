# DEVELOP

from bs4 import BeautifulSoup as soup
# import csv
import pandas as pd
# import os
import functions as fnc


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}

rtb_url_list = ['https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=6&year=1214',
                'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=1217',
                'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=221&year=1238']


def returnDataFrameRTB(url: str):
    from bs4 import BeautifulSoup

    p = BeautifulSoup(fnc.downloadWebsite(url, headers), 'lxml')

    names = []
    values = []
    sources = []
    years = []

    y = p.find('span', id='ctl00_mainContent_LBLYear')
    year = y.text

    source = p.find('span', id='ctl00_mainContent_LBLSite')

    for brand_item in p.findAll('div', class_='name'):
        for name in brand_item.findAll('a'):
            i = name.text.strip()
            names.append(i)

    for valuation in p.findAll('div', class_='weighted'):
        i = valuation.text.strip()
        i_converted = i.replace(',', '.')

        if i_converted.isdigit() or fnc.isFloat(i_converted):
            values.append(i)

    for i in names:
        sources.append(source.text)
        years.append(year)

    tuples = list(zip(names, values, sources, years))

    df = pd.DataFrame(tuples, columns=['NAME', 'VALUE', 'SOURCE', 'YEAR'])

    print(df)

    return df


def getUrlListRTB(url: str, hdr: dict) -> dict:  # gets all the URLs for each year from each ranking --> returns a dictionary (year: "url")
    from bs4 import BeautifulSoup

    d = {}
    sliced_link = url[:(len(url) - 4)]

    p = BeautifulSoup(fnc.downloadWebsite(url, hdr), 'lxml')

    o = p.findAll('option')

    for i in o:
        f = sliced_link + i['value']
        d[str(i.text)] = f

    return d


def concatDataFramesRTB(url: list, hdr: dict, outputName: str):

    l = list()
    links = list()

    for i in url:
        z = getUrlListRTB(i, hdr)
        for a, b in z.items():
            l.append(returnDataFrameRTB(b))

    f = pd.concat(l)

    f.to_csv(outputName, index=False, header=False)


# TESTING
