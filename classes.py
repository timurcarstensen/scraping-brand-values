# DEVELOPMENT BRANCH
import pandas as pd
import functions as fnc

readIn = pd.read_excel('raw.xlsx')  # reading in the sorted.xlsx file and creating a new DataFrame
readIn = readIn.loc[:, ~readIn.columns.str.contains('^Unnamed')]

class Row(object):
    def __init__(self, name: str, sources: [str], year: int):
        self.name = name
        self.year = year
        self.sources = sources


    def returnRowDF(self, d: dict()): # takes in a dict from the 'Brand' class and returns a single row as a dataframe
        import pandas as pd
        my_dict = dict()
        df1 = pd.DataFrame({'NAME': [self.name], 'YEAR': [self.year]})
        df2 = pd.DataFrame()
        for i in self.sources:       
            v = list()
            try:
                v = [v for (y, v) in d[i] if y == self.year]
            except Exception:
                pass
            if len(v) != 0:
                my_dict[i] = v
            else: 
                my_dict[i] = ['NaN']
        
        df2 = pd.DataFrame(my_dict)

        df = pd.concat([df1,df2], axis=1)
        
        return df


class Brand(object):
    import pandas as pd
    from row_class import Row

    def __init__(self, name: str, frame: pd.DataFrame): 
        self.name = name
        self.frame = frame
        self.currentSources = [] # sources for each specific brand
        self.allSources = [] # all sources available in self.frame
        self.d = {}
        self.yearList = []
        self.findYearSourceCombinations()
        self.country = str() # to be added later
        self.sector = str() # to be added later
        self.concatDataFrames

    def getValue(self, source: str, year: int) -> str: #gets value for specific source and year of 
        f = self.frame
        n = self.name
        v = f.loc[(f.NAME == n) & (f.SOURCE == source) & (f.YEAR == year)].VALUE.item()
        return int(v)
    
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
        self.findYearsSources()
        f = self.returnBrandDataFrame()
        s = self.currentSources
        for i in s: 
            l = []
            x = f.loc[f.SOURCE == i].YEAR.sort_values(ascending=True)
            for y in x: 
                l.append(tuple((y, self.getValue(i, y))))
            self.d[i] = l    

    def concatDataFrames(self):
        l = list()
        for i in self.yearList:
            r = Row(self.name, fnc.getSources(self.frame), i)
            l.append(r.returnRowDF(self.d))
        
        df = pd.concat(l)
        return df
