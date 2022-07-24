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
papki
##
df = pd.read_excel(base_path + f'/Вологодская обл..xlsx')
df = drop_num(df=df)
# df = drop_num_2(df=df)
df['наименование_субъекта'] = re.sub(r'[xls.]', '', papki[0])
print(df)
##
pd.options.display.max_columns = None
pd.options.display.width = 5000
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
    if str(y).lower().strip().startswith(('проведен профессиональный', 'проведено психофизио', 'всего', '(6000)',
                                          'продолжение')):
        df7.drop(index=[x], inplace=True)
df7.dropna(inplace=True, axis=0, subset=['1'])
df7.reset_index(inplace=True, drop=True)
if df7.shape[0] == 0:
    df7.loc[0, :] = np.nan
del df7['наименование_субъекта']
for x, y in enumerate(df7_1['1']):
    if str(y).lower().strip().startswith(('проведено освидетельст', 'всего', '(6000)', '19.03.20', '15.03.20',
                                          'продолжение')):
        df7_1.drop(index=[x], inplace=True)
df7_1.dropna(inplace=True, axis=0, subset=['1'])
df7_1.reset_index(inplace=True, drop=True)
if df7_1.shape[0] == 0:
    df7_1.loc[0, :] = np.nan
df7 = pd.concat([df7, df7_1], ignore_index=True, axis=1)
df7.shape
##
df7
##
print(df[365:375])
##

##
df8
##
if len(a) != 2:
    df8 = pd.DataFrame({'1': np.nan,
                        '2': np.nan,
                        '3': np.nan,
                        '4': np.nan,
                        '5': np.nan,
                        '6': np.nan,
                        '7': np.nan,
                        '8': np.nan,
                        'наименование_субъекта': np.nan}, index=[0])
    df8.loc[:, :] = np.nan
else:

    df8.dropna(axis=1, how='all', inplace=True)
df8.reset_index(drop=True, inplace=True)
a = 0
for x, y in enumerate(df8.values):
    for i, j in enumerate(df8.values[x]):
        try:
            isinstance(int(j), int)
            a += 1
            df8_1 = pd.DataFrame(df8.loc[x, :]).T
        except:
            if a > 0:
                break
            else:
                continue
    if a > 0:
        break
if 'df8_1' not in locals():
    df8_1 = pd.DataFrame(df8.loc[0, :]).T
    df8_1.loc[0, :] = np.nan
df8_1.reset_index(drop=True, inplace=True)
df8_1.rename(columns={
    '1': 'проведено_учебных_циклов',
    '2': 'обучено_всего',
    '3': 'обучено_оргздав',
    '4': 'обучено_СМП',
    '5': 'обучено_МЧС_РФ',
    '6': 'обучено_МВД_РФ',
    '7': 'обучено_МПС_РФ',
    '8': 'обучено_прочие'}, inplace=True)
df8_1.loc[0, 'наименование_субъекта'] = re.sub(r'[xls.]', '', os.path.basename(base_path + f'/{papki[0]}'))
