from bs4 import BeautifulSoup as soup
import csv
import urllib.request as uReq
import pandas as pd
import os
import all_functions as fnc

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent': user_agent}


url_list = ['https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=83&year=1200',
            'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=6&year=1214',
            'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=1217',
            'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=221&year=1238']

for i in url_list:

    url_dictionary = fnc.get_url_list(i)

    csvFileNames = []
    currentTitle = ''

    print(url_dictionary)

    for key, value in url_dictionary.items():

        brandNames = []
        brandValues = []

        website = uReq.Request(value, headers=headers)

        uClient = uReq.urlopen(website)  # downloading the website
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, 'lxml')

        if currentTitle == '':
            currentTitle = page_soup.title.text.strip() # [0:32] + page_soup.title.text.strip()[39:48]

        fileName = key + '.csv'
        csvFileNames.append(fileName)

        csv_file = open(fileName, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Brandname', 'Valuation'])

        for brand_item in page_soup.findAll('div', class_='name'):
            for name in brand_item.findAll('a'):
                i = name.text.strip()
                brandNames.append(i)

        for valuation in page_soup.findAll('div', class_='weighted'):
            i = valuation.text.strip()
            i_converted = i.replace(',', '.')

            if i_converted.isdigit() or fnc.isfloat(i_converted):
                brandValues.append(i)

        dictionary = dict(zip(brandNames, brandValues))

        for keys, values in dictionary.items():
            csv_writer.writerow([keys, values])

        csv_file.close()

        print('done with: ' + key)

    writer = pd.ExcelWriter(currentTitle + '.xlsx', engine='xlsxwriter')

    for files in csvFileNames:
        dataFrame = pd.read_csv(files)
        dataFrame.to_excel(writer, sheet_name=files[0:4])
        os.remove(files)

    writer.save()

    print(currentTitle + '.xlsx')
    print('Finished')
