# DEVELOP

from bs4 import BeautifulSoup as soup
# import csv
import pandas as pd
# import os
import functions as fnc


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}

url_list = ['https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=83&year=1200',
            'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=6&year=1214',
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

    t = p.find('span', id='ctl00_mainContent_LBRankName')
    l = t.text

    source = l.split(' ')[0]

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
        sources.append(source)
        years.append(year)

    tuples = list(zip(names, values, sources, years))

    df = pd.DataFrame(tuples, columns=['NAME', 'VALUE', 'SOURCE', 'YEAR'])

    print(df)

    return df


def getUrlListRTB(url: str) -> dict:  # gets all the URLs for each year from each ranking --> returns a dictionary (year: "url")
    from bs4 import BeautifulSoup
    import urllib.request as uReq

    u_dict = {}
    link_length = len(url)
    sliced_link = url[:(link_length - 4)]

    website = uReq.Request(url, headers=headers)

    uClient = uReq.urlopen(website)
    page_html = uClient.read()
    uClient.close()

    soup = BeautifulSoup(page_html, 'lxml')

    option = soup.findAll('option')

    for i in option:
        formattedLink = sliced_link + i['value']
        u_dict[i.text] = formattedLink

    return u_dict
