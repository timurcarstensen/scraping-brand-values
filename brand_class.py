import pandas as pd

readIn = pd.read_excel('sorted.xlsx')  # reading in the sorted.xlsx file and creating a new DataFrame
readIn = readIn.loc[:, ~readIn.columns.str.contains('^Unnamed')]


class Brand(object):
    import pandas as pd

    def __init__(self, name: str, frame: pd.DataFrame): 
        self.name = name
        self.frame = frame
        self.sourceList = []
        self.d = {'': [()]}
        self.yearList = []
        self.sourceList = []
        self.findYearSourceCombinations()

    def checkSources(self):
        pass

    def getValue(self, source: str, year: int) -> str:
        f = self.frame
        n = self.name
        v = f.loc[(f.NAME == n) & (f.SOURCE == source) & (f.YEAR == year)].VALUE.item()
        return str(v)
    
    def returnBrandDataFrame(self) -> pd.DataFrame:
        f = self.frame
        n = self.name
        return f.loc[f.NAME == n]

    def findYearsSources(self):
        sL = []
        yL = []
        for x, y in self.returnBrandDataFrame().iterrows():
            if y.SOURCE not in sL: 
                sL.append(y.SOURCE)
            if y.YEAR not in yL:
                yL.append(y.YEAR)
        yL.sort()
        self.yearList = yL
        self.sourceList = sL

    def findYearSourceCombinations(self):
        my_dict = self.d
        self.findYearsSources()
        f = self.returnBrandDataFrame()
        s = self.sourceList
        for i in s: 
            l = []
            x = f.loc[f.SOURCE == i].YEAR.sort_values(ascending=True)
            for y in x: 
                l.append(tuple((y, self.getValue(i, y))))
            my_dict[i] = l
        self.d = my_dict
                
                
my_brand = Brand('Amazon', readIn)

for x, y in my_brand.d.items():
    print(x,y)




