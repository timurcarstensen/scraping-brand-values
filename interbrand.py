import functions as fnc
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}


def getUrlDictInterbrand(url: str) -> dict:
    d = dict()

    rng = range(2000, 2019)
    for i in rng:
        s = url[:39] + str(i) + url[62:]
        d[i] = s

    return d


def returnDataFrameInterbrand(url: str, hdr: dict):
    from bs4 import BeautifulSoup

    p = BeautifulSoup(fnc.downloadWebsite(url, hdr), 'lxml')

    names = []
    values = []
    sources = []
    years = []

    y = p.find('div', class_='col-50 left copyright-year text-tiny')
    x = y.text
    src = x.strip()
    source = src[7:17]
    year = int(src[2:6])

    for b in p.findAll('li', class_='brand-item'):
        for n in b.find('div', class_='brand-info brand-name brand-col-4'):
            i = n.strip()
            names.append(i)

        for z in b.find('div', class_='brand-info brand-value brand-col-7'):
            i = z.strip()
            values.append(i)

    for i in names:
        sources.append(source)
        years.append(year)

    brand_tuples = list(zip(names, values, sources, years))

    df = pd.DataFrame(brand_tuples, columns=['name', 'value', 'source', 'year'])

    print(df)

    return df
