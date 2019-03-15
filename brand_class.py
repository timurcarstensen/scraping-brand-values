# DEVELOPMENT BRANCH
import pandas as pd

readIn = pd.read_excel('sorted.xlsx')  # reading in the sorted.xlsx file and creating a new DataFrame
readIn = readIn.loc[:, ~readIn.columns.str.contains('^Unnamed')]


class Brand(object):
    import pandas as pd

    def __init__(self, name: str, frame: pd.DataFrame): 
        self.name = name
        self.frame = frame
        self.currentSources = [] # sources for each specific brand
        self.allSources = [] # all sources available in self.frame
        self.d = {'': [()]}
        self.yearList = []
        self.findYearSourceCombinations()
        self.country = str() # to be added later
        self.sector = str() # to be added later

    def checkSources(self):
        pass

    def getValue(self, source: str, year: int) -> str: #gets value for specific source and year of 
        f = self.frame
        n = self.name
        v = f.loc[(f.NAME == n) & (f.SOURCE == source) & (f.YEAR == year)].VALUE.item()
        return str(v)
    
    def returnBrandDataFrame(self) -> pd.DataFrame:
        f = self.frame
        n = self.name
        return f.loc[f.NAME == n]

    def findYearsSources(self):
        f = self.frame
        sL = []
        yL = []
        for x, y in self.returnBrandDataFrame().iterrows():
            if y.SOURCE not in sL: 
                sL.append(y.SOURCE)
            if y.YEAR not in yL:
                yL.append(y.YEAR)
        yL.sort()
        for i in f.SOURCE:
            if i not in self.allSources:
                self.allSources.append(i)
        self.yearList = yL
        self.currentSources = sL

    def findYearSourceCombinations(self):
        my_dict = self.d
        self.findYearsSources()
        f = self.returnBrandDataFrame()
        s = self.currentSources
        for i in s: 
            l = []
            x = f.loc[f.SOURCE == i].YEAR.sort_values(ascending=True)
            for y in x: 
                l.append(tuple((y, self.getValue(i, y))))
            my_dict[i] = l
        self.d = my_dict
                
                
for i in readIn.NAME:
    x = Brand(i, readIn)
    print(x.name) 
    for index, row in x.d.items():
        print(index, row)




# my_brand = Brand('Apple', readIn)

# for x, y in my_brand.d.items():
#     print(x,y)