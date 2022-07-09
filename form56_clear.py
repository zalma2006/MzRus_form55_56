##
import os
import pandas as pd
import re
from other_function import drop_num, drop_num_2

base_path = r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2017 ' \
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
            y.lower().strip() == 'профили медицинской помощи':
        a.append(x)
    if type(y) == str and y.lower().startswith('прочие') and len(a) > 0:
        a.append('stop')
        a.append(x + 1)
    if 'stop' in a:
        break
df56_4_1 = df[a[0]:a[-1]].copy()

df56_4_1.dropna(axis=1, how='all', inplace=True)
df56_4_1.dropna(axis=0, subset=['1'], inplace=True)
df56_4_1.reset_index(drop=True, inplace=True)
df56_4_1.drop(index=[0], inplace=True)
df56_4_1.reset_index(drop=True, inplace=True)
df56_4_1['1'] = df56_4_1['1'].str.strip()
del df56_4_1['наименование_субъекта']
for x, y in enumerate(df56_4_1.columns):
    if y != '1':
        df56_4_1[y] = df56_4_1[y].astype(str)
        df56_4_1[y] = df56_4_1[y].str.replace(',', '.')
        df56_4_1[y] = df56_4_1[y].str.extract(r'(\d+)')
        df56_4_1[y] = df56_4_1[y].astype(float)
a = []
for x, y in enumerate(df['1']):
    if type(y) == str and \
            y.lower().strip() == 'профили медицинской помощи':
        a.append(x)
    if type(y) == str and y.lower().startswith('прочие') and len(a) > 0:
        a.append(x + 1)
df56_4_2 = df[a[-3]:a[-1]].copy()
df56_4_2.dropna(axis=1, how='all', inplace=True)
df56_4_2.dropna(axis=0, subset=['1'], inplace=True)
df56_4_2.reset_index(drop=True, inplace=True)
df56_4_2.drop(index=[0, 1], inplace=True)
df56_4_2.reset_index(drop=True, inplace=True)
del df56_4_2['1']
for x, y in enumerate(df56_4_2.columns):
    if y != 'наименование_субъекта':
        df56_4_2[y] = df56_4_2[y].astype(str)
        df56_4_2[y] = df56_4_2[y].str.replace(',', '.')
        df56_4_2[y] = df56_4_2[y].str.extract(r'(\d+)')
        df56_4_2[y] = df56_4_2[y].astype(float)
df56_4 = pd.concat([df56_4_1, df56_4_2], ignore_index=True, axis=1)
df56_4.rename(columns={
    0: 'профили_МП',
    1: 'оказана_ЭКМП_всего',
    2: 'оказана_ЭКМП_детям',
    3: 'оказана_ЭКМП_детям_до_года',
    4: 'оказана_ЭКМП_ПострадЧС_всего',
    5: 'оказана_ЭКМП_ПострадЧС_детей',
    6: 'оказана_ЭКМП_ПострадЧС_детей_до_года',
    7: 'эвакуировано_всего',
    8: 'эвакуировано_детей',
    9: 'эвакуировано_детей_до_года',
    10: 'эвакуировано_ПострадЧС_всего',
    11: 'эвакуировано_ПострадЧС_детей',
    12: 'эвакуировано_ПострадЧС_детей_до_года',
    13: 'эвакуировано_вРегМО_всего',
    14: 'эвакуировано_вРегМО_детей',
    15: 'эвакуировано_вРегМО_детей_до_года',
    16: 'эвакуировано_вРегМО_ПострадЧС_всего',
    17: 'эвакуировано_вРегМО_ПострадЧС_детей',
    18: 'эвакуировано_вРегМО_ПострадЧС_детей_до_года',
    19: 'эвакуировано_вМежРегМО_всего',
    20: 'эвакуировано_вМежРегМО_детей',
    21: 'эвакуировано_вМежРегМО_детей_до_года',
    22: 'эвакуировано_вМежРегМО_ПострадЧС_всего',
    23: 'эвакуировано_вМежРегМО_ПострадЧС_детей',
    24: 'эвакуировано_вМежРегМО_ПострадЧС_детей_до_года',
    25: 'эвакуировано_вФедМО_всего',
    26: 'эвакуировано_вФедМО_детей',
    27: 'эвакуировано_вФедМО_детей_до_года',
    28: 'эвакуировано_вФедМО_ПострадЧС_всего',
    29: 'эвакуировано_вФедМО_ПострадЧС_детей',
    30: 'эвакуировано_вФедМО_ПострадЧС_детей_до_года',
    31: 'наименование_субъекта'}, inplace=True)

##
df56_4
##
pd.options.display.max_columns = None
##
a
##
a = []
for x, y in enumerate(df['1']):
    if type(y) == str and \
            y.lower().strip() == 'профили медицинской помощи':
        a.append(x)
    if type(y) == str and y.lower().startswith('прочие') and len(a) > 0:
        a.append(x + 1)
df56_4_2 = df[a[-3]:a[-1]].copy()

df56_4_2.dropna(axis=1, how='all', inplace=True)
df56_4_2.dropna(axis=0, subset=['1'], inplace=True)
df56_4_2.reset_index(drop=True, inplace=True)
df56_4_2.drop(index=[0, 1], inplace=True)
df56_4_2.reset_index(drop=True, inplace=True)
df56_4_2.rename(columns={
    '1': 'профили_МП',
    '2': 'оказана_ЭКМП_всего',
    '3': 'оказана_ЭКМП_детям',
    '4': 'оказана_ЭКМП_детям_до_года',
    '5': 'оказана_ЭКМП_ПострадЧС_всего',
    '6': 'оказана_ЭКМП_ПострадЧС_детей',
    '7': 'оказана_ЭКМП_ПострадЧС_детей_до_года',
    '8': 'эвакуировано_всего',
    '9': 'эвакуировано_детей',
    '10': 'эвакуировано_детей_до_года',
    '11': 'эвакуировано_ПострадЧС_всего',
    '12': 'эвакуировано_ПострадЧС_детей',
    '13': 'эвакуировано_ПострадЧС_детей_до_года'}, inplace=True)
df56_4_2['профили_МП'] = df56_4_2['профили_МП'].str.strip()
for x, y in enumerate(df56_4_2.columns):
    if y not in ['профили_МП', 'наименование_субъекта']:
        df56_4_2[y] = df56_4_2[y].astype(str)
        df56_4_2[y] = df56_4_2[y].str.replace(',', '.')
        df56_4_2[y] = df56_4_2[y].str.extract(r'(\d+)')
        df56_4_2[y] = df56_4_2[y].astype(float)
##
df56_4_2
##