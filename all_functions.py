def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_url_list(url: str) -> dict:
    from bs4 import BeautifulSoup
    from urllib.request import urlopen as uReq
    u_dict = {}
    link_length = len(url)
    sliced_link = url[:(link_length - 4)]

    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    soup = BeautifulSoup(page_html, 'lxml')

    option = soup.findAll('option')

    for i in option:
        formattedLink = sliced_link + i['value']
        u_dict[i.text] = formattedLink

    return u_dict






