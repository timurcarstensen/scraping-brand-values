# DEVELOPMENT BRANCH

'''-------IMOPORTING MODULES--------'''
from bs4 import BeautifulSoup
import pandas as pd

'''--------GLOBAL VARIABLES-------------'''
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}

'''-----------------GLOBAL FUNCTIONS----------------------'''

def isFloat(value): #checks if a number (or string) is a floating point
    try:
        float(value)
        return True
    except ValueError:
        return False


def downloadWebsite(link: str, hdr: dict) -> str:
    import urllib.request as uReq
    from bs4 import BeautifulSoup

    website = uReq.Request(link, headers=hdr)
    uClient = uReq.urlopen(website)  # downloading the website
    page_html = uClient.read()
    uClient.close()
    return page_html


def toExcel(name: str, df): #saves dataframe to .xlsx file
    import pandas as pd
    w = pd.ExcelWriter(name + '.xlsx')
    df.to_excel(w, 'Sheet1', index=False)
    w.save()

def getSources(frame: pd.DataFrame) -> list: # returns all unique sources in a given dataframe as a list
    my_list = list()
    for i in frame.SOURCE:
        if i not in my_list:
            my_list.append(i)
    return my_list

def getNames(frame: pd.DataFrame) -> list: # returns all unique brand names in any given dataframe as a list
    l = list()
    for i in frame.NAME:
        if i not in l:
            l.append(i)
    return l
    
'''----------------------------BRANDFINANCE FUNCTIONS-------------------------------''' 

def returnUrlDictBrandDirectory(url: str) -> dict:  # takes in a initial url and retuns a dictionary (Year : Corresponding link)
    u_dict = dict()
    # link = url[:(len(url) - 4)]

    for i in range(2007, 2020):
        if i == 2007:  # adding exception for the year 2007 as the link format is slightly different
            z = 'https://brandirectory.com/league_tables/table/global-250-2007'
            u_dict[i] = z
        else:
            x = url[:(len(url) - 4)] + str(i)
            u_dict[i] = x

    return u_dict


def returnDataFrameBrandDirectory(url: str, hdr: dict):  # takes a link (string) and a header (dictionary) and returns a dataframe
    from bs4 import BeautifulSoup as soup
    p = soup(downloadWebsite(url, hdr), 'lxml')

    y = int(url[-4:])
    s = 'BrandFinance'

    names = list()
    values = list()
    sources = list()
    years = list()

    for x in p.findAll('span'):
        print(x)
        # for i in x.find('a', class_='tight-text'):
        #     print(i)
        #     print(i)
        #     if len(names) <= 99: #for i in x.value:     find('a'):
        #         names.append(i)

    for v in p.findAll('td', attrs={"data-label": y}):
        print(v)
        # for i in v.findAll('span', class_='o'):
        #     values.append(i.text.replace(',', ''))

    for i in names:
        sources.append(s)
        years.append(y)

    tuples = list(zip(names, values, sources, years))

    df = pd.DataFrame(tuples, columns=['NAME', 'VALUE', 'SOURCE', 'YEAR'])

    print('done with ' + str(y) + '!')

    return df


def concatDataFramesWriteCsvBrandFinance(url: str, headers: dict, outputName: str):
    l = list()

    for y in returnUrlDictBrandDirectory(url).values():
        l.append(returnDataFrameBrandDirectory(y, headers))

    f = pd.concat(l)
    f.to_csv(outputName, index=False, header=False)

'''---------------------RANKING THE BRANDS FUNCTIONS-----------------------'''

def returnDataFrameRTB(url: str):
    from bs4 import BeautifulSoup as soup

    p = soup(downloadWebsite(url, headers), 'lxml', from_encoding='utf-8') # from_encoding='utf-8' to properly parse all the brand names

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
        if source.text == 'Millward Brown':
            i = valuation.text.strip()
            i = i.replace(',', '')
            i = i.replace('.', '')
            if i.isdigit() or isFloat(i):
                values.append(int(i))
        
        elif "Forbes" in source.text:
            i = valuation.text.strip()
            if '.' in i:
                i = i.replace('.', '')
                i = i + '00'
            else:
                i = i + '000'
            if i.isdigit() or isFloat(i):
                values.append(int(i))

        elif source.text == 'European Brand Institute - Vienna':
            i = valuation.text.strip()
            i_c = i.replace('.', '')
            if i_c.isdigit() or isFloat(i_c):
                values.append(int(i_c))

        elif 'Brand Finance' in source.text:
            i = valuation.text.strip()
            i = i.replace('.', '')
            i = i.replace(',', '')
            if i.isdigit() or isFloat(i):
                values.append(int(i))

    for i in names:
        sources.append(source.text)
        years.append(int(year))

    tuples = list(zip(names, values, sources, years))

    df = pd.DataFrame(tuples, columns=['NAME', 'VALUE', 'SOURCE', 'YEAR'])

    print('done with ' + str(year) + '!')

    return df


def getUrlListRTB(url: str, hdr: dict) -> dict:  # gets all the URLs for each year from each ranking -> returns a dictionary (year: "url")
    from bs4 import BeautifulSoup as soup

    d = {}
    sliced_link = url[:(len(url) - 4)]

    p = soup(downloadWebsite(url, hdr), 'lxml')

    o = p.findAll('option')

    for i in o:
        f = sliced_link + i['value']
        d[str(i.text)] = f

    return d


def concatDataFramesRTB(url: list, hdr: dict, outputName: str):

    l = list()
    # links = list()

    for i in url:
        z = getUrlListRTB(i, hdr)
        for b in z.values():
            l.append(returnDataFrameRTB(b))

    f = pd.concat(l)

    f.to_csv(outputName, index=False, header=False)

'''----------------------------INTERBRAND FUNCTIONS----------------------------------'''

def getUrlDictInterbrand(url: str) -> dict:
    d = dict()

    rng = range(2000, 2019)
    for i in rng:
        s = url[:58] + str(i) + url[62:]
        d[i] = s

    return d


def returnDataFrameInterbrand(url: str, hdr: dict, currentYear: int):
    from bs4 import BeautifulSoup as soup
    p = soup(downloadWebsite(url, hdr), 'lxml')  # scrapes data off website and returns dataframe with the values

    names = []
    values = []
    sources = []
    years = []

    source = p.find('div', class_='col-50 left copyright-year text-tiny').text.strip()[7:17]  # finds the current source

    for b in p.findAll('li', class_='brand-item'):  # loop over all brands and collect name and brand value
        for n in b.find('div', class_='brand-info brand-name brand-col-4'):
            names.append(n.strip())

        for z in b.find('div', class_='brand-info brand-value brand-col-7'):
            z = z.replace('$m', '')
            z = z.replace(',', '')
            z = z.strip()
            values.append(int(z))

    for i in names:  # adding as many sources (in this case just Interbrand as this is the interbrand function) and the currentYear into a list
        sources.append(source)
        years.append(currentYear)

    brand_tuples = list(zip(names, values, sources, years))  # using all the lists to create tuples with 4 arguments

    df = pd.DataFrame(brand_tuples, columns=['NAME', 'VALUE', 'SOURCE', 'YEAR'])  # using the tuple which we created above to create a dataframe

    # print(df)

    print('done with ' + str(currentYear) + '!')

    return df


# TESTING CODE


def concatDataFramesWriteCsvInterbrand(url: str, headers: dict, outputName: str):
    l = list()

    for x, y in getUrlDictInterbrand(url).items():

        l.append(returnDataFrameInterbrand(y, headers, x))

    f = pd.concat(l)
    f.to_csv(outputName, index=False, header=False)