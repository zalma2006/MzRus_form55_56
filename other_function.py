# удаляем из таблицы строки с номерами столбцов в каждой
# из таблиц для таблиц у которых нет столбца с номерами строк: таблица 7
import pandas as pd
import datetime
import os
from clear_function_df import *


def drop_num(df):
    col_names = dict(zip(df.columns.tolist(),
                         list(map(str, range(1, len(df.columns) + 1)))))
    df.rename(columns=col_names, inplace=True)
    df.dropna(how='all', inplace=True)
    df.drop(index=df[(df['1'].isin(['1', 1, '11', 11])) &
                     (df['2'].isin(['2', 2, '12', 12])) &
                     (df['3'].isin(['3', 3, '13', 13]))].index, axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# удаляем из таблицы столбцы с номерами строк в каждой из таблиц
def drop_num_2(df):
    for x, y in enumerate(df.columns):
        a = 0
        if df[df[y] == '№ строки'].shape[0] > 0:
            a += 1
            del df[y]
        if a > 0:
            break
    col_names = dict(zip(df.columns.tolist(),
                         list(map(str, range(1, len(df.columns) + 1)))))
    df.rename(columns=col_names, inplace=True)
    return df


# сохраняем готовый файл
def save_df(df, papka, z, base_path):
    os.chdir(os.getcwd() + f'/переработанные файлы/{papka}')
    a = re.sub(r'[xls.]', '', z)
    df.to_excel(os.getcwd() + f'/{a}.xlsx', index=False)
    os.chdir(base_path)
    return


# функция очистки по 1 году
def clear_df(base_path):
    start_time = datetime.datetime.now()
    os.chdir(base_path)
    files = [x for x in os.listdir() if x.endswith(('.xlsx', '.xls',))]

    for x, y in enumerate(files):
        df = pd.read_excel(base_path + f'/{files[x]}', engine='openpyxl')
        df = drop_num(df)
        df['наименование_субъекта'] = re.sub(r'[xls.]', '', files[x])
        df7 = find_df7(df, y)
        df8 = find_df8(df, y)
        df = drop_num_2(df)
        del df[df.columns[-1]]
        df['наименование_субъекта'] = re.sub(r'[xls.]', '', files[x])
        df1 = find_df1(df, y)
        df2 = find_df2(df, y)
        df3 = find_df3(df, y)
        df4 = find_df4(df)
        df5 = find_df5(df)
        df6 = find_df6(df)
        df9 = find_df9(df)
        df10 = find_df10(df)
        df11 = find_df11(df, y)
        save_df(df1, r'Табл_сведения_о_центре_МК', y, base_path)
        save_df(df2, r'Сведения_о_кадрах_мк', y, base_path)
        save_df(df3, r'Формирования_мк', y, base_path)
        save_df(df4, r'Сведения_о_пострадавших_ЧС', y, base_path)
        save_df(df5, r'Сведения_о_видах_помощи_вЧС', y, base_path)
        save_df(df6, r'Использование_КФ_приЧС', y, base_path)
        save_df(df7, r'Сведения_о_лаборатории_мк', y, base_path)
        save_df(df8, r'Сведения_о_обучении', y, base_path)
        save_df(df9, r'Сведения_о_учениях_трениров_занят', y, base_path)
        save_df(df10, r'Сведения_о_трассовых_пунктах', y, base_path)
        save_df(df11, r'Сведения_о_МТО_МК', y, base_path)
        if x in [20, 40, 60, 80]:
            print(f'сделано {x} файлов')
    a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
    b = datetime.datetime.now() - start_time
    print(f'''Время затраченное на выполнение очищения и сохранения 55 формы отчётности
    за {a} год составило {round(b.total_seconds(), 2)} сек.''')
