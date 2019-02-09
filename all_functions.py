def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_url_list(url: str) -> dict:
    from bs4 import BeautifulSoup
    import urllib.request as uReq

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}


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






