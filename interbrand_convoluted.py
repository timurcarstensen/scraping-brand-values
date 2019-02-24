from bs4 import BeautifulSoup as soup
import csv
from urllib.request import urlopen as uReq
import pandas as pd
import os
import functions as fnc

csvFileNames = []

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}


# for url in urlList:

#     fileNameCSV = url[58:62] + '.csv'
#     csvFileNames.append(fileNameCSV)

#     csv_file = open(fileNameCSV, 'w')
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(['Brandname', 'Valuation'])

#     uClient = uReq(url)
#     page_html = uClient.read()
#     uClient.close()

#     page_soup = soup(page_html, 'lxml')

#     brandNames = []
#     brandValues = []

#     for brand_item in page_soup.findAll('li', class_='brand-item'):
#         for name in brand_item.find('div', class_='brand-info brand-name brand-col-4'):
#             i = name.strip()
#             brandNames.append(i)

#         for value in brand_item.find('div', class_='brand-info brand-value brand-col-7'):
#             i = value.strip()
#             brandValues.append(i)

#     dictionary = dict(zip(brandNames, brandValues))

#     for key, value in dictionary.items():

#         csv_writer.writerow([key, value])

#     csv_file.close()

#     print('done with: ' + url[58:62])

# writer = pd.ExcelWriter('interbrand_global_top_brands_all_years.xlsx', engine='xlsxwriter')

# for files in csvFileNames:

#     dataframe = pd.read_csv(files)
#     dataframe.to_excel(writer, sheet_name=files[0:4])
#     os.remove(files)

# writer.save()

# print('Finished')


def getUrlDictInterbrand(url: str) -> dict:
    d = dict()

    rng = range(2000, 2019)
    for i in rng:
        s = url[:58] + str(i) + url[62:]
        d[i] = s

    return d


def returnDataFrameInterbrand(url: str, hdr: dict):
    from bs4 import BeautifulSoup

    p = soup(fnc.downloadWebsite(url, hdr), 'lxml')

    names = []
    values = []
    sources = []
    years = []

    y = p.find('div', class_='col-50 left copyright-year text-tiny')
    x = y.text
    src = x.strip()
    source = src[7:17]

    yearFind = p.find('h1', class_='bottom-line').text.strip()[19:23]

    print(yearFind)

    # year = int(src[2:6])

    for b in p.findAll('li', class_='brand-item'):
        for n in b.find('div', class_='brand-info brand-name brand-col-4'):
            i = n.strip()
            names.append(i)

        for z in b.find('div', class_='brand-info brand-value brand-col-7'):
            i = z.strip()
            values.append(i)

    for i in names:
        sources.append(source)
        # years.append(year)

    brand_tuples = list(zip(names, values, sources, years))

    df = pd.DataFrame(brand_tuples, columns=['name', 'value', 'source', 'year'])

    # print(df)

    return df


dictionary = getUrlDictInterbrand('https://www.interbrand.com/best-brands/best-global-brands/2018/ranking/')

for x, y in dictionary.items():
    returnDataFrameInterbrand(y, headers)
