import pandas as pd  # importing pandas
import functions as fnc  # importing functions file

readIn = pd.read_excel('sorted.xlsx')  # reading in the sorted.xlsx file and creating a new DataFrame
readIn = readIn.loc[:, ~readIn.columns.str.contains('^Unnamed')]

sources = []
names = []
testDict = {}

for index, row in readIn.iterrows(): 
    if row['SOURCE'] not in sources:
        sources.append(row['SOURCE'])

readOut = pd.DataFrame({'NAME': [], 'YEAR': []})

def checkIfNaN(n: str, src: str, y: int, i: pd.DataFrame) -> bool:
    i.loc[(i.NAME == n) & (i.YEAR == y) & (i.)]



    
    myBool = True
    return myBool
    


# for i in sources:
#     readOut[i] = 'NaN'

# for index, row in readIn.iterrows(): 
#     if row['NAME'] not in names: 
#         names.append(row['NAME'])

# dfList = []

# for index, row in readIn.iterrows():
#     r = pd.DataFrame({'NAME': [], 'YEAR': []}) #creating empty dataframe
#     for i in sources: # adding columns to dataframe
#         r[i] = 'NaN'



    
    
