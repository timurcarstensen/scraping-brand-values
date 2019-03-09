import pandas as pd  # importing pandas
import functions as fnc  # importing functions file

readIn = pd.read_excel('sorted.xlsx')  # reading in the sorted.xlsx file and creating a new DataFrame
readIn = readIn.loc[:, ~readIn.columns.str.contains('^Unnamed')]

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

new_df = pd.DataFrame({'NAME': nameList, 'YEAR': yearList})  # creating a new DataFrame based upon brand names and all unique years

new_df['Country'] = 'NaN'  # adding a column for country
new_df['Industry Sector'] = 'NaN'  # adding a column for industry sector

for i in sources:  # adding new columns for each source available
    new_df[i] = 'NaN'

columnList = list(new_df)

currentBrand = str()
currentYear = int()
currentSource = str()


# fnc.toExcel('testing', new_df)
