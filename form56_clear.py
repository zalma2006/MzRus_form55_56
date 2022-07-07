##
import os
import pandas as pd
import re
from other_function import drop_num, drop_num_2

base_path = r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2015 ' \
            r'г/ФОРМА 56/для_программы'
papki = [x for x in os.listdir(base_path) if x.endswith(('.xls', '.xlsx'))]
##
df = pd.read_excel(base_path + f'/{papki[0]}')
df = drop_num(df=df)
df = drop_num_2(df=df)
df['наименование_субъекта'] = re.sub(r'[xls.]', '', papki[0])
print(df)


def find_df56_2(df):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and y.lower().lstrip().startswith('наименование должностей'):
            a.append(x)
        if type(y) == str and y.lower().startswith('всего должностей') and len(a) > 0:
            a.append(x + 1)
        if len(a) == 2:
            break
    df56_2 = df[a[0]:a[-1]].copy()
    df56_2.dropna(axis=1, how='all', inplace=True)
    df56_2.reset_index(drop=True, inplace=True)
    for x, y in enumerate(df56_2['1']):
        if str(y).lower().startswith('врачи - в'):
            df56_2 = df56_2[x:].copy()
            break
    df56_2.rename(columns={
        '1': 'наименование_должностей',
        '2': 'число_штатных_должностей',
        '3': 'число_занятых_должностей',
        '4': 'числоФЛ_оснРаботников',
        '5': 'имеют_статус_спасателя',
        '6': 'имеют_ВысшКвалКатегорию',
        '7': 'имеют_ПерКвалКатегорию',
        '8': 'имеют_ВторКвалКатегорию'}, inplace=True)
    for x, y in enumerate(df56_2.columns):
        if df56_2[y].dtypes == object:
            try:
                df56_2[y] = df56_2[y].str.replace(',', '.')
            except:
                continue
            try:
                df56_2[y] = df56_2[y].astype(float)
            except:
                continue
    return df56_2


##
df56_2 = find_df56_2(df)
df56_2
##
df56_2.info()
##
