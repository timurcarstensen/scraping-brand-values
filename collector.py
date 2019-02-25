import pandas as pd
import numpy as np


fileName = 'BUSI2118.xlsx'

df = pd.read_excel(fileName)


print(df.values)
