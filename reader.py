import pandas as pd  # importing pandas
import functions as fnc  # importing functions file

readIn = pd.read_excel('sorted.xlsx')  # reading in the sorted.xlsx file and creating a new DataFrame
readIn = readIn.loc[:, ~readIn.columns.str.contains('^Unnamed')]


def getValueFromReadIn(brandName: str, year: int, source: str, input: pd.DataFrame) -> str:
    import pandas as pd
    v = str(input.loc[(input.NAME == brandName) & (input.YEAR == year) & (input.SOURCE == source)].iloc[0]['VALUE'])
    return v

names = []
yearList = []
nameList = []
sources = []

for i in readIn.NAME:  # finding all unique names in the read in DataFrame
    if i not in names:
        names.append(i)

for name in names:  # Extracting all years available for each brand in the ranking
    nL = []
    yL = []
    x = readIn[readIn.NAME == name].sort_values(by=['YEAR'])
    for z in x.YEAR:
        if z not in yL:
            yL.append(z)
    for y in range(len(yL)):
        nL.append(name)
    for i in yL:
        yearList.append(i)
    for i in nL:
        nameList.append(i)

for i in readIn.SOURCE:  # finding all unique sources
    if i not in sources:
        sources.append(i)

readOut = pd.DataFrame({'NAME': nameList, 'YEAR': yearList})  # creating a new DataFrame based upon brand names and all unique years

readOut['Country'] = 'NaN'  # adding a column for country
readOut['Industry Sector'] = 'NaN'  # adding a column for industry sector

for i in sources:  # adding new columns for each source available
    readOut[i] = 'NaN'

columnList = list(readOut)

d = list()


for index, row in readOut.iterrows():
    for source in sources:
        n = row['NAME']
        y = row['YEAR']
        for s in sources:
                if row[s] == 'NaN':
                        try:
                            k = getValueFromReadIn(row['NAME'], row['YEAR'], s, readIn)
                            if k not in d: 
                                d.append(k)
                        except:
                                pass


