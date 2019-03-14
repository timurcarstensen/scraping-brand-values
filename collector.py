import pandas as pd
import functions as fnc

dfList = list()

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}

interbrandUrl = 'https://www.interbrand.com/best-brands/best-global-brands/2018/ranking/'

# brandFinanceUrl = 'https://brandirectory.com/league_tables/table/global-500-2018'

rtbUrlList = ['https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=6&year=1214',
                'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=1217',
                'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=221&year=1238',
                'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=83&year=1250']


# for x, y in fnc.returnUrlDictBrandDirectory(brandFinanceUrl).items():
#     dfList.append(fnc.returnDataFrameBrandDirectory(y, headers))

for x, y in fnc.getUrlDictInterbrand(interbrandUrl).items():
    dfList.append(fnc.returnDataFrameInterbrand(y, headers, x))

for i in rtbUrlList:
    for x, y in fnc.getUrlListRTB(i, headers).items():
        dfList.append(fnc.returnDataFrameRTB(y))

f = pd.concat(dfList)

f = f.sort_values(by=['NAME', 'SOURCE', 'YEAR'])

fnc.toExcel('raw', f) # takes concatonated dataframes (f) and saves them to excel

