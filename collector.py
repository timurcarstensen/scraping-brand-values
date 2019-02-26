import pandas as pd
import interbrand_df as inter
import brandfinance_df as brand
import rtb_df as rtb

dfList = list()

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}

interbrand_url = 'https://www.interbrand.com/best-brands/best-global-brands/2018/ranking/'

brandfinance_url = 'https://brandirectory.com/league_tables/table/global-500-2018'

rtb_url_list = ['https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=6&year=1214',
                'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=334&year=1217',
                'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=221&year=1238']


for x, y in inter.getUrlDictInterbrand(interbrand_url).items():
    dfList.append(inter.returnDataFrameInterbrand(y, headers, x))

for x, y in brand.returnUrlDictBrandDirectory(brandfinance_url).items():
    dfList.append(brand.returnDataFrameBrandDirectory(y, headers))


for i in rtb_url_list:
    for x, y in rtb.getUrlListRTB(i, headers).items():
        dfList.append(rtb.returnDataFrameRTB(y))

f = pd.concat(dfList)

writer = pd.ExcelWriter('final.xlsx')

f.to_excel(writer, 'Sheet1', index=False)
writer.save()

f.to_csv('final.csv', index=False, header=False)
