##
import os
import pandas as pd
import re
import numpy as np
from other_function import drop_num, drop_num_2

base_path = r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2020 ' \
            r'г/ФОРМА 55/для программы'
papki = [x for x in os.listdir(base_path) if x.endswith(('.xls', '.xlsx'))]
##
df = pd.read_excel(base_path + f'/{papki[0]}')
df = drop_num(df=df)
df = drop_num_2(df=df)
df['наименование_субъекта'] = re.sub(r'[xls.]', '', papki[0])
print(df)

##
a = []
for x, y in enumerate(df['1']):
    if type(y) == str and \
            y.lower().lstrip().startswith('трассовые пункты всего'):
        a.append(x)
    if type(y) == str and \
            y.lower().startswith('из них умерших во время санитарно-авиационной эвакуации всего') \
            and len(a) > 0:
        a.append(x + 2)
    if len(a) == 2:
        break
df10 = df[a[0]:a[-1]].copy()
df10.dropna(axis=1, how='all', inplace=True)
df10.reset_index(drop=True, inplace=True)
if '2' not in df10.columns:
    df10['2'] = np.nan
    df10 = df10[['1', '2', 'наименование_субъекта']]
df10.rename(columns={
    '1': 'показатели_о_деят_трасспунктов',
    '2': 'число'}, inplace=True)
for x, y in enumerate(df10.columns):
    if df10[y].dtypes == object:
        df10[y] = df10[y].str.replace(',', '.')
    try:
        df10[y] = df10[y].astype(float)
    except:
        continue


df10.shape
##
df10
##
pd.options.display.max_columns = None
##