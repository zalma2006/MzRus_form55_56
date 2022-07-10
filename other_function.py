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
def save_df(df, papka, z, base_path, forma):
    if forma == 55:
        os.chdir(os.getcwd() + f'/переработанные файлы/{papka}')
        a = re.sub(r'[xls.]', '', z)
        df.to_excel(os.getcwd() + f'/{a}.xlsx', index=False)
        os.chdir(base_path)
    if forma == 56:
        os.chdir(os.getcwd() + f'/переработанные_файлы/{papka}')
        a = re.sub(r'[xls.]', '', z)
        df.to_excel(os.getcwd() + f'/{a}.xlsx', index=False)
        os.chdir(base_path)


# функция очистки по 1 году
def clear_df(base_path, forma, problems):
    if forma == 55:
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
            if df1.shape[0] != 14 or df1.shape[1] != 3:
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Табл_сведения_о_центре_МК'] = [f'его размеры {df1.shape}, а должны быть (14, 3)']
            df2 = find_df2(df, y)
            if df2.shape[0] != 43 or df2.shape[1] != 9:
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Табл_сведения_о_центре_МК'] = [f'его размеры {df2.shape}, а должны быть (43, 9)']
            df3 = find_df3(df, y)
            if ((df3.shape[0] != 56 or df3.shape[1] != 6) and
                    (''.join(re.findall(r'\d+', base_path.split(r'/')[-3])) == '2015')) or\
                    ((df3.shape[0] != 60 or df3.shape[1] != 6) and
                     (''.join(re.findall(r'\d+', base_path.split(r'/')[-3])) != '2015')):
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Табл_сведения_о_центре_МК'] = [f'его размеры {df3.shape}, а должны быть '
                                                                      f' для 2015 г (56, 6) а для 2016 г. (60, 6)']
            df4 = find_df4(df)
            if df4.shape[0] != 53 or df4.shape[1] != 19:
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Табл_сведения_о_центре_МК'] = [f'его размеры {df4.shape}, '
                                                                      f'а должны быть (53, 19)']
            df5 = find_df5(df)
            if df5.shape[0] != 53 or df5.shape[1] != 18:
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Табл_сведения_о_центре_МК'] = [f'его размеры {df5.shape}, '
                                                                      f'а должны быть (53, 18)']
            df6 = find_df6(df)
            if df6.shape[0] != 17 or df6.shape[1] != 10:
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Табл_сведения_о_центре_МК'] = [f'его размеры {df6.shape}, '
                                                                      f'а должны быть (17, 10)']
            df9 = find_df9(df)
            if df9.shape[0] != 14 or df9.shape[1] != 6:
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Табл_сведения_о_центре_МК'] = [f'его размеры {df9.shape}, '
                                                                      f'а должны быть (14, 6)']
            df10 = find_df10(df)
            if df10.shape[0] != 14 or df10.shape[1] != 6:
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Табл_сведения_о_центре_МК'] = [f'его размеры {df10.shape}, '
                                                                      f'а должны быть (14, 6)']
            df11 = find_df11(df, y)
            save_df(df1, r'Табл_сведения_о_центре_МК', y, base_path, forma)
            save_df(df2, r'Сведения_о_кадрах_мк', y, base_path, forma)
            save_df(df3, r'Формирования_мк', y, base_path, forma)
            save_df(df4, r'Сведения_о_пострадавших_ЧС', y, base_path, forma)
            save_df(df5, r'Сведения_о_видах_помощи_вЧС', y, base_path, forma)
            save_df(df6, r'Использование_КФ_приЧС', y, base_path, forma)
            save_df(df7, r'Сведения_о_лаборатории_мк', y, base_path, forma)
            save_df(df8, r'Сведения_о_обучении', y, base_path, forma)
            save_df(df9, r'Сведения_о_учениях_трениров_занят', y, base_path, forma)
            save_df(df10, r'Сведения_о_трассовых_пунктах', y, base_path, forma)
            save_df(df11, r'Сведения_о_МТО_МК', y, base_path, forma)
            if x in [20, 40, 60, 80]:
                print(f'сделано {x} файлов')
        a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
        b = datetime.datetime.now() - start_time
        print(f'''Время затраченное на выполнение очищения и сохранения 55 формы отчётности
        за {a} год составило {round(b.total_seconds(), 2)} сек.''')
    if forma == 56:
        start_time = datetime.datetime.now()
        os.chdir(base_path)
        files = [x for x in os.listdir() if x.endswith(('.xlsx', '.xls',))]

        for x, y in enumerate(files):
            df = pd.read_excel(base_path + f'/{files[x]}', engine='openpyxl')
            df = drop_num(df)
            df = drop_num_2(df)
            df['наименование_субъекта'] = re.sub(r'[xls.]', '', files[x])
            df56_1 = find_df56_1(df)
            if df56_1.shape[0] != 13 or df56_1.shape[1] != 3:
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Сведения_отдЭКМПиМЭ'] = [f'его размеры {df56_1.shape}, а должны быть (13, 3)']
            df56_2 = find_df56_2(df)
            if df56_2.shape[0] != 19 or df56_2.shape[1] != 9:
                a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                b = re.sub(r'[xls.]', '', files[x])
                problems[f'{b} - {a} - Кадры_отдЭКМПиМЭ'] = [f'его размеры {df56_2.shape}, а должны быть (19, 9)']
            if base_path not in [r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                                 r'(2015-2020гг)/2015 г/ФОРМА 56/для_программы',
                                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                                 r'(2015-2020гг)/2016 г/ФОРМА 56/для_программы']:
                df56_3 = find_df56_3_no1516(df=df, z=y)
                if df56_3.shape[0] != 23 or df56_3.shape[1] != 24:
                    a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                    b = re.sub(r'[xls.]', '', files[x])
                    problems[f'{b} - {a} - Деятельность_отдЭКМПиМЭ'] = [f'его размеры {df56_3.shape}, '
                                                                        f'а должны быть (23, 24)']
            if base_path == r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 ' \
                            r'(2015-2020гг)/Ф.55,56 (2015-2020гг)/2015 г/ФОРМА 56/для_программы':
                df56_3 = find_df56_3_2015(df)
                if df56_3.shape[0] != 30 or df56_3.shape[1] != 17:
                    a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                    b = re.sub(r'[xls.]', '', files[x])
                    problems[f'{b} - {a} - Деятельность_отдЭКМПиМЭ'] = [f'его размеры {df56_3.shape}, '
                                                                        f'а должны быть (30, 17)']
            if base_path == r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 ' \
                            r'(2015-2020гг)/2016 г/ФОРМА 56/для_программы':
                df56_3 = find_df56_3_2016(df=df, z=y)
                if df56_3.shape[0] != 25 or df56_3.shape[1] != 24:
                    a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                    b = re.sub(r'[xls.]', '', files[x])
                    problems[f'{b} - {a} - Деятельность_отдЭКМПиМЭ'] = [f'его размеры {df56_3.shape}, '
                                                                        f'а должны быть (25, 24)']
            if base_path not in [r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                                 r'(2015-2020гг)/2015 г/ФОРМА 56/для_программы',
                                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                                 r'(2015-2020гг)/2016 г/ФОРМА 56/для_программы']:
                df56_4 = find_df56_4_no1516(df)
                if df56_4.shape[0] != 16 or df56_4.shape[1] != 32:
                    a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                    b = re.sub(r'[xls.]', '', files[x])
                    problems[f'{b} - {a} - Выезды_отдЭКМПиМЭ'] = [f'его размеры {df56_4.shape}, а должны быть (16, 32)']
            if base_path in [r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                             r'(2015-2020гг)/2015 г/ФОРМА 56/для_программы',
                             r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                             r'(2015-2020гг)/2016 г/ФОРМА 56/для_программы']:
                df56_4 = find_df56_4_1516(df)
                if ((df56_4.shape[0] != 16 or df56_4.shape[1] != 22) and \
                        (''.join(re.findall(r'\d+', base_path.split(r'/')[-3])) == '2015')) or \
                        ((df56_4.shape[0] != 19 or df56_4.shape[1] != 22) and
                         (''.join(re.findall(r'\d+', base_path.split(r'/')[-3])) != '2015')):
                    a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
                    b = re.sub(r'[xls.]', '', files[x])
                    problems[f'{b} - {a} - Выезды_отдЭКМПиМЭ'] = [f'его размеры {df56_4.shape}, а должны быть (16, 22) '
                                                                  f'в 2015 году и (19, 22) в 2016 году']

            save_df(df=df56_1, papka=r'Сведения_отдЭКМПиМЭ', z=y, base_path=base_path, forma=forma)
            save_df(df=df56_2, papka=r'Кадры_отдЭКМПиМЭ', z=y, base_path=base_path, forma=forma)
            save_df(df=df56_3, papka=r'Деятельность_отдЭКМПиМЭ', z=y, base_path=base_path, forma=forma)
            save_df(df=df56_4, papka=r'Выезды_отдЭКМПиМЭ', z=y, base_path=base_path, forma=forma)
            if x in [20, 40, 60, 80]:
                print(f'сделано {x} файлов')
        a = ''.join(re.findall(r'\d+', base_path.split(r'/')[-3]))
        b = datetime.datetime.now() - start_time
        print(f'''Время затраченное на выполнение очищения и сохранения 56 формы отчётности
        за {a} год составило {round(b.total_seconds(), 2)} сек.''')
    return problems