import pandas as pd  # importing pandas
import functions as fnc  # importing functions file

readIn = pd.read_excel('sorted.xlsx')  # reading in the sorted.xlsx file and creating a new DataFrame
readIn = readIn.loc[:, ~readIn.columns.str.contains('^Unnamed')]


try:
    print(readIn.loc[(readIn.NAME == 'Amazon') & (readIn.YEAR == 2010) & (readIn.SOURCE == 'Interbrand')])
except AttributeError:
    print('wrong attribute')
except Exception as e:
    print(type(e))


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

df = pd.DataFrame({'NAME': nameList, 'YEAR': yearList})  # creating a new DataFrame based upon brand names and all unique years

df['Country'] = 'NaN'  # adding a column for country
df['Industry Sector'] = 'NaN'  # adding a column for industry sector

for i in sources:  # adding new columns for each source available
    df[i] = 'NaN'

columnList = list(df)

# currentBrand = str()
# currentYear = int()
# currentSource = str()

# for i in names:
#     y = df.loc[df.NAME == i]
#     cY = int()
#     for i in y.YEAR:
#         print(i)


# fnc.toExcel('testing', new_df)


