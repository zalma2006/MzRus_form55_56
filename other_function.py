# удаляем из таблицы строки с номерами столбцов в каждой
# из таблиц для таблиц у которых нет столбца с номерами строк: таблица 7
import pandas as pd
import datetime
import os
import re
from clear_function_df import *
def drop_num(df, z):
    col_names = dict(zip(df.columns.tolist(),
                         list(map(str, range(1, len(df.columns)+1)))))
    df.rename(columns=col_names, inplace=True)
    df.dropna(how='all', inplace=True)
    df.drop(index=df[(df['1'].isin(['1', 1, '11', 11]))&
                     (df['2'].isin(['2', 2, '12', 12]))&
                     (df['3'].isin(['3', 3, '13', 13]))].index, axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    col_names = dict(zip(df.columns.tolist(),
                         list(map(str, range(1, len(df.columns)+1)))))
    df.rename(columns=col_names, inplace=True)
    return df
# удаляем из таблицы столбцы с номерами строк в каждой из таблиц
def drop_num_2(df, z):
    for x, y in enumerate(df.columns):
        a = 0
        if df[df[y] == '№ строки'].shape[0] > 0:
            a += 1
            del df[y]
        if a > 0:
            break
    col_names = dict(zip(df.columns.tolist(),
                         list(map(str, range(1, len(df.columns)+1)))))
    df.rename(columns=col_names, inplace=True)
    return df

# сохраняем готовый файл
def save_df(df, papka, z):
    os.chdir(os.getcwd() + f'/переработанные файлы/{papka}')
    a = re.sub(r'[xls.]', '', files[z])
    df.to_excel(os.getcwd() + f'/{a}.xlsx', index=False)
    os.chdir(base_path)
    return


# функция очистки по 1 году
def clear_df(base_path):
    start_time = datetime.datetime.now()
    os.chdir(base_path)
    files = [x for x in os.listdir() if x.endswith(('.xlsx', '.xls',))]

    for x, y in enumerate(files):
        df = pd.read_excel(base_path + f'/{files[x]}', engine="openpyxl", thousands=',')
        df = drop_num(df, x)
        df['наименование_субъекта'] = re.sub(r'[xls.]', '', files[x])
        df7 = find_df7(df, x)
        df8 = find_df8(df, x)
        df = drop_num_2(df, x)
        del df[df.columns[-1]]
        df['наименование_субъекта'] = re.sub(r'[xls.]', '', files[x])
        df1 = find_df1(df, x)
        df2 = find_df2(df, x)
        df3 = find_df3(df, x)
        df4 = find_df4(df, x)
        df5 = find_df5(df, x)
        df6 = find_df6(df, x)
        df9 = find_df9(df, x)
        df10 = find_df10(df, x)
        df11 = find_df11(df, x)
        save_df(df1, r'Табл_сведения_о_центре_МК', x)
        save_df(df2, r'Сведения_о_кадрах_мк', x)
        save_df(df3, r'Формирования_мк', x)
        save_df(df4, r'Сведения_о_пострадавших_ЧС', x)
        save_df(df5, r'Сведения_о_видах_помощи_вЧС', x)
        save_df(df6, r'Использование_КФ_приЧС', x)
        save_df(df7, r'Сведения_о_лаборатории_мк', x)
        save_df(df8, r'Сведения_о_обучении', x)
        save_df(df9, r'Сведения_о_учениях_трениров_занят', x)
        save_df(df10, r'Сведения_о_трассовых_пунктах', x)
        save_df(df11, r'Сведения_о_МТО_МК', x)
    a = ''.join(re.findall('\d+', base_path.split(r'/')[-3]))
    b = datetime.datetime.now() - start_time
    print(f'''Время затраченное на выполнение очищения и сохранения 55 формы отчётности
    за {a} год составило {round(b.total_seconds(), 2)} сек.''')