import pandas as pd
df = pd.read_excel('sorted.xlsx')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

names = list()

brandDict = {'': []}

for i in df.NAME:
    if i not in names:
        names.append(i)

for i in names:
    l = []
    x = df[df.NAME == i].sort_values(by=['YEAR'])
    for z in x.YEAR:
        if z not in l:
            l.append(z)
    brandDict[i] = l

# new = pd.DataFrame.from_dict(brandDict, orient='index')

my_list = pd.Series(brandDict['Amazon'])

new_df = pd.DataFrame(my_list)
print(new_df)
