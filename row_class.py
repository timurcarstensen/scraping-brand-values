# DEVELOPMENT BRANCH

class Row(object):
    def __init__(self, name: str, sources: [str], year: int):
        self.name = name
        self.year = year
        self.sources = sources

    def addSourceValue(self, source: str, value: int):
        pass