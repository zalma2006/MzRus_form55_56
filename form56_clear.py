##
import os
import pandas as pd
import re
from other_function import drop_num, drop_num_2

base_path = r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2016 ' \
            r'г/ФОРМА 56/для_программы'
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
            str(y).lower().strip() == 'наименования':
        a.append(x)
    if type(y) == str and str(y).lower().startswith('медицинских грузов, тонны') and len(a) > 1:
        a.append('stop')
        a.append(x + 1)
    if 'stop' in a:
        break
df56_3_1 = df[a[0]:a[-1]].copy()
df56_3_1.dropna(axis=1, how='all', inplace=True)
df56_3_1.dropna(axis=0, subset=['1'], inplace=True)
df56_3_1.reset_index(drop=True, inplace=True)
for x, y in enumerate(df56_3_1['1']):
    if str(y).lower().strip() == 'наименования':
        df56_3_1.drop(index=[x], inplace=True)
df56_3_1.reset_index(drop=True, inplace=True)
a = []
for x, y in enumerate(df['1']):
    if type(y) == str and \
            str(y).lower().strip() == 'наименования' and \
            str(df.at[x-1, '1']).lower().strip().startswith('медицинских грузов'):
        a.append(x)
    if type(y) == str and str(y).lower().startswith('медицинских грузо') and len(a) > 0:
        a.append(x + 1)
    if len(a) == 2:
        break
df56_3_2 = df[a[0]:a[-1]].copy()
df56_3_2.dropna(axis=1, how='all', inplace=True)
df56_3_2.dropna(axis=0, subset=['1'], inplace=True)
df56_3_2.reset_index(drop=True, inplace=True)
for x, y in enumerate(df56_3_2['1']):
    if str(y).lower().strip() == 'наименования' or str(y).strip() == '1':
        df56_3_2.drop(index=[x], inplace=True)
df56_3_2.reset_index(drop=True, inplace=True)
df56_3 = pd.concat([df56_3_1, df56_3_2], axis=1, ignore_index=True)
del df56_3[14], df56_3[15]
df56_3.rename(columns={
    0: 'наименование',
    1: 'оказана_МП_всего',
    2: 'оказана_МП_детям',
    3: 'оказана_МП_детям_до_года',
    4: 'оказана_МП_ОснРаботниками',
    5: 'оказана_МП_НаДогоспит_всего',
    6: 'оказана_МП_НаДогоспит_детям',
    7: 'оказана_МП_НаДогоспит_детям_до_года',
    8: 'оказана_МП_НаДогоспит_ПострадЧС_всего',
    9: 'оказана_МП_НаДогоспит_ПострадЧС_детям',
    10: 'оказана_МП_НаДогоспит_ПострадЧС_детям_до_года',
    11: 'оказана_МП_НаДогоспит_ПострадДТП_всего',
    12: 'оказана_МП_НаДогоспит_ПострадДТП_детям',
    13: 'оказана_МП_НаДогоспит_ПострадДТП_детям_до_года',
    16: 'оказана_МП_НаСтационар_всего',
    17: 'оказана_МП_НаСтационар_детям',
    18: 'оказана_МП_НаСтационар_детям_до_года',
    19: 'оказана_МП_НаСтационар_ПострадЧС_всего',
    20: 'оказана_МП_НаСтационар_ПострадЧС_детям',
    21: 'оказана_МП_НаСтационар_ПострадЧС_детям_до_года',
    22: 'оказана_МП_НаСтационар_ПострадДТП_всего',
    23: 'оказана_МП_НаСтационар_ПострадДТП_детям',
    24: 'оказана_МП_НаСтационар_ПострадДТП_детям_до_года',
    25: 'наименование_субъекта'}, inplace=True)
df56_3['наименование'] = df56_3['наименование'].str.strip()
for x, y in enumerate(df56_3.columns):
    if y not in ['наименование', 'наименование_субъекта']:
        df56_3[y] = df56_3[y].astype(str)
        df56_3[y] = df56_3[y].str.replace(',', '.')
        df56_3[y] = df56_3[y].str.extract(r'(\d+)')
        df56_3[y] = df56_3[y].astype(float)


##
df56_3
##
pd.options.display.max_columns = None
##
a
##