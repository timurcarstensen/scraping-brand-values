# this is the develop branch

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

    brand_tuples = list(zip(names, values, sources, years

                            ))

    df = pd.DataFrame(brand_tuples, columns=['name', 'value', 'source', 'year'])

    # print(df)

    return df


dict = fnc.getUrlListRTB('https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=6&year=1214')

dictOfDataFrames = {}

for x, y in dict.items():
    dictOfDataFrames[x] = returnDataFrameRTB(y)

print(dictOfDataFrames)


# p = soup(fnc.downloadWebsite(url_list[0], headers), 'lxml')

# t = p.find('span', id='ctl00_mainContent_LBRankName')
# l = t.text

# title = l.split(' ')

# print(title[0])


# def dwnld_rtb_ranking_rtn_df(url: str) -> [DataFrame]:
#     frames = []
#     url_dictionary = fnc.get_url_list(url)

#     for x, y in url_dictionary.items():
#         page = soup(fnc.download_website(y, headers), 'lxml')

# for i in url_list:

#     url_dictionary = fnc.get_url_list(i)

#     csvFileNames = []
#     currentTitle = ''

#     for key, value in url_dictionary.items():

#         brandNames = []
#         brandValues = []

#         page_soup = soup(fnc.download_website(value, headers), 'lxml')

#         if currentTitle == '':
#             currentTitle = page_soup.title.text.strip()  # [0:32] + page_soup.title.text.strip()[39:48]

#         fileName = key + '.csv'
#         csvFileNames.append(fileName)

#         csv_file = open(fileName, 'w')
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(['Brandname', 'Valuation'])

#         for brand_item in page_soup.findAll('div', class_='name'):
#             for name in brand_item.findAll('a'):
#                 i = name.text.strip()
#                 brandNames.append(i)

#         for valuation in page_soup.findAll('div', class_='weighted'):
#             i = valuation.text.strip()
#             i_converted = i.replace(',', '.')

#             if i_converted.isdigit() or fnc.isfloat(i_converted):
#                 brandValues.append(i)

#         dictionary = dict(zip(brandNames, brandValues))

#         for keys, values in dictionary.items():
#             csv_writer.writerow([keys, values])

#     csv_file.close()

#     print('done with: ' + key)

# writer = pd.ExcelWriter(currentTitle + '.xlsx', engine='xlsxwriter')

# for files in csvFileNames:
#     dataFrame = pd.read_csv(files)
#     dataFrame.to_excel(writer, sheet_name=files[0:4])
#     os.remove(files)

# writer.save()

# print(currentTitle + '.xlsx')
# print('Finished')


# def list_of_tuples(soup) -> [()]:
#     tuples = []
#     tpl = tuple()
#     name = ""
#     value = 0

#     for items in soup.findAll('div', class_='name'):

#     for brand_item in soup.findAll('div', class_='name'):
#         for name in brand_item.findAll('a'):
#             i = name.text.strip()
#             name = i

#     for valuation in soup.findAll('div', class_='weighted'):
#         i = valuation.text.strip()
#         i.replace(',', '.')

#         if i.isdigit() or fnc.isfloat(i):
#             value = i
#     tpl = (name, value)

#     return tuples
