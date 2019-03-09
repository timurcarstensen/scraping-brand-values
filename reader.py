import pandas as pd # importing pandas
import functions as fnc # importing functions file

readIn = pd.read_excel('sorted.xlsx') # reading in the sorted.xlsx file and creating a new DataFrame
readIn = readIn.loc[:, ~readIn.columns.str.contains('^Unnamed')]

names = []
yearList = []
nameList = []
sources = []

for i in readIn.NAME:
    if i not in names:
        names.append(i)

for name in names:
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

for i in readIn.SOURCE:
    if i not in sources:
        sources.append(i)

new_df = pd.DataFrame({'NAME': nameList, 'YEAR': yearList})

new_df['Country'] = "NaN"
new_df['Industry Sector'] = "NaN"

for i in sources:
    new_df[i] = 'NaN'

# fnc.toExcel('testing', new_df)



