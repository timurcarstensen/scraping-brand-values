# DEVELOP

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}


def isFloat(value):
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


def toExcel(name: str, df):
    import pandas as pd
    w = pd.ExcelWriter(name + '.xlsx')
    df.to_excel(w, 'Sheet1', index=False)
    w.save()