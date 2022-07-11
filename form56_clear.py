##
import os
import pandas as pd
import re
import numpy as np
from other_function import drop_num, drop_num_2

base_path = r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2015 ' \
            r'г/ФОРМА 55/для программы'
papki = [x for x in os.listdir(base_path) if x.endswith(('.xls', '.xlsx'))]
##
df = pd.read_excel(base_path + f'/{papki[0]}')
df = drop_num(df=df)
# df = drop_num_2(df=df)
df['наименование_субъекта'] = re.sub(r'[xls.]', '', papki[0])
print(df)

##
a = []
for x, y in enumerate(df['1']):
    if type(y) == str and y.lower().lstrip().startswith('проведен профессиональный'):
        a.append(x)
    if type(y) == str and y.lower().startswith('проведено освидетель'):
        a.append(x + 5)
    if len(a) == 2:
        break
df7 = df[a[0]:a[-1] - 5].copy()
df7_1 = df[a[-1] - 5:a[-1]].copy()
df7.dropna(axis=1, how='all', inplace=True)
df7_1.dropna(axis=1, how='all', inplace=True)
df7.reset_index(drop=True, inplace=True)
df7_1.reset_index(drop=True, inplace=True)
for x, y in enumerate(df7['1']):
    if str(y).lower().strip().startswith(('проведен профессиональный','проведено психофизио', 'всего', '(6000)')):
        df7.drop(index=[x], inplace=True)
df7.dropna(inplace=True, axis=0, subset=['1'])
df7.reset_index(inplace=True, drop=True)
if df7.shape[0] == 0:
    df7.loc[0, :] = np.nan
del df7['наименование_субъекта']
for x, y in enumerate(df7_1['1']):
    if str(y).lower().strip().startswith(('проведено освидетельст', 'всего', '(6000)', '19.03.20')):
        df7_1.drop(index=[x], inplace=True)
df7_1.dropna(inplace=True, axis=0, subset=['1'])
df7_1.reset_index(inplace=True, drop=True)
if df7_1.shape[0] == 0:
    df7_1.loc[0, :] = np.nan
df7 = pd.concat([df7, df7_1], ignore_index=True, axis=1)
df7.rename(columns={
    0: 'Проведен_психофизтест_всего',
    1: 'Проведен_психофизтест_сотруд_АСФ',
    2: 'Проведен_психофизтест_сотруд_СМК',
    3: 'Проведен_психофизтест_волонтёров',
    4: 'Из_них_годных',
    5: 'Из_них_условногодных',
    6: 'Проведена_психокоррекция_всего',
    7: 'Проведена_психокоррекция_сотруд_АСФ',
    8: 'Проведена_психокоррекция_сотруд_СМК',
    9: 'Проведена_психокоррекция_волонтёров',
    10: 'Проведено_освидетел_всего',
    11: 'Проведено_освидетел_сотруд_АСФ',
    12: 'Проведено_освидетел_сотруд_СМК',
    13: 'Прошедшие_психреабилитацию_всего',
    14: 'Прошедшие_психреабилитацию_сотруд_АСФ',
    15: 'Прошедшие_психреабилитацию_сотруд_СМК',
    16: 'Прошедшие_психреабилитацию_прочие',
    17: 'Число_психпомощи_населению_в_повседдеятельности',
    18: 'Число_психпомощи_населению_в_ЧС',
    19: 'Число_психпомощи_населению_ТМК_онлайн',
    20: 'наименование_субъекта'}, inplace=True)
for x, y in enumerate(df7.columns):
    if y != 'наименование_субъекта':
        df7[y] = df7[y].astype(str)
        df7[y] = df7[y].str.replace(',', '.')
        df7[y] = df7[y].astype(float)

df7.shape
##
df7
##
pd.options.display.max_columns = None
##