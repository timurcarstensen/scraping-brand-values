# develop


class Brand:

    v = dict()

    def __init__(self, name, value, source):
        self.name = name

    def add_year_value(self, year, value, src):
        self.v[year] = [value, src]


apple_brand = Brand('Apple', '300000000', 'Brandfinance.com')

apple_brand.add_year_value(1998, 3000, "Brandfinance")
apple_brand.add_year_value(1997, 3330, "Interbrand")


print(apple_brand.v)
