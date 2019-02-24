# this is the develop branch

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}


def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


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


def downloadWebsite(link: str, hdr: dict) -> str:
    import urllib.request as uReq

    website = uReq.Request(link, headers=hdr)
    uClient = uReq.urlopen(website)  # downloading the website
    page_html = uClient.read()
    uClient.close()
    return page_html
