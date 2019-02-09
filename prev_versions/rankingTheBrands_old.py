from bs4 import BeautifulSoup as soup
import csv
from urllib.request import urlopen as uReq
import pandas as pd
import os
from all_functions import isfloat

urlList = ['https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=1217',
           'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=1161',
           'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=1053',
           'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=933',
           'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=866',
           'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=714']

years = ['2018', '2017', '2016', '2015', '2014', '2013']
yearsComplex = []
csvFileNames = []
currentTitle = ''

for i in urlList:
    yearsComplex.append(i[76:])

yearDictionary = dict(zip(years, yearsComplex))

for url in urlList:

    brandNames = []
    brandValues = []

    uClient = uReq(url)  # downloading the website
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, 'lxml')

    if currentTitle == '':
        currentTitle = page_soup.title.text.strip()[0:32] + page_soup.title.text.strip()[39:48]

    currentYearClx = page_soup.find('span', {'id': 'ctl00_mainContent_LBLYear'})
    currentYear = currentYearClx.text.strip()

    fileName = currentYear + '.csv'
    csvFileNames.append(fileName)

    csv_file = open(fileName, 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Brandname', 'Valuation'])

    for brand_item in page_soup.findAll('div', class_='name'):
        for name in brand_item.findAll('a'):
            i = name.text.strip()
            brandNames.append(i)

    for value in page_soup.findAll('div', class_='weighted'):
        i = value.text.strip()

        if isfloat(i):
            brandValues.append(i)

    dictionary = dict(zip(brandNames, brandValues))

    for key, value in dictionary.items():
        csv_writer.writerow([key, value])

    csv_file.close()

    print('done with: ' + currentYear)

writer = pd.ExcelWriter(currentTitle + '.xlsx', engine='xlsxwriter')

for files in csvFileNames:
    dataFrame = pd.read_csv(files)
    dataFrame.to_excel(writer, sheet_name=files[0:4])
    os.remove(files)

writer.save()

print(currentTitle + '.xlsx')
print('Finished')
