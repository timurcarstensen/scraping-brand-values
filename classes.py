# develop


class Brand:
    def __init__(self, name, value, source):
        self.name = name
        self.value = value
        self.source = source


apple_brand = Brand('Apple', '300000000', 'Brandfinance.com')

print(apple_brand.source)
