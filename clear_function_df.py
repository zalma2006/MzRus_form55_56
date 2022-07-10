import pandas as pd
import re
import numpy as np


# поиск 1 таблицы (сведения о центре МК)
def find_df1(df, z):
    a = []
    b = 0
    for x, y in enumerate(df['1']):
        if type(y) == str and y.lower().startswith('наименование') and \
                (str(df.loc[x, '2']).startswith('Отметка (нет') or
                 str(df.loc[x, '3']).startswith('Отметка (нет') or
                 str(df.loc[x, '4']).startswith('Отметка (нет')):
            a.append(x)
            b += 1
        if type(y) == str and y.lower().startswith('прочий'):
            a.append(x + 1)
            b += 1
        if b >= 2:
            break
    df1 = df[a[0]: a[-1]].copy()
    df1.dropna(how='all', axis=1, inplace=True)
    df1.reset_index(drop=True, inplace=True)
    col_names = dict(zip(df1.columns.tolist(), df1.loc[0, :].values.tolist()))
    df1.drop(index=0, inplace=True)
    df1.rename(columns=col_names, inplace=True)
    df1.rename(columns={re.sub(r'[xls.]', '', z): 'наименование_субъекта'}, inplace=True)
    df1.loc[df1[df1[df1.columns[1]].isna()].index, df1.columns[1]] = 0
    df1.loc[df1[df1[df1.columns[1]].isin([1, '1'])].index, df1.columns[1]] = 1
    df1[df1.columns[1]] = df1[df1.columns[1]].astype(int)
    for x, y in enumerate(df1.columns):
        if y not in [df1.columns[0], 'наименование_субъекта']:
            df1[y] = df1[y].astype(str)
            df1[y] = df1[y].str.replace(',', '.')
            df1[y] = df1[y].astype(float)
    return df1


# Кадры службы МК
def find_df2(df, z):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and y.lower().lstrip().startswith('наименование должн') and \
                (str(df.loc[x, '2']).lower().startswith('число должност') or
                 str(df.loc[x, '3']).lower().startswith('число должност') or
                 str(df.loc[x, '4']).lower().startswith('число должност')) and len(a) != 1:
            a.append(x)
        if type(y) == str and y.lower().startswith('всего должност'):
            a.append(x + 1)
        if len(a) == 2:
            break
    df2 = df[a[0]:a[-1]].copy()
    df2.dropna(axis=1, how='all', inplace=True)
    df2.reset_index(inplace=True, drop=True)
    for x, y in enumerate(df2.loc[0, :]):
        if str(y).lower().startswith('число должнос') and \
                str(y).lower() != 'число должностей штатных':
            df2.iloc[0, x] = 'число должностей штатных'
        if str(y) in ['nan', 'NaN', 'Nan'] and df2.iloc[1, x].lower().startswith('занят'):
            df2.iloc[0, x] = 'число должностей занятых'
        if str(y).lower().startswith('имеют квалификационн') and \
                df2.iloc[1, x].lower().startswith('высш'):
            df2.iloc[0, x] = 'имеют квалификационную категорию из гр. 5 высшую'
        if str(y) in ['nan', 'NaN', 'Nan'] and df2.iloc[1, x].lower().startswith('перв'):
            df2.iloc[0, x] = 'имеют квалификационную категорию из гр. 5 первую'
        if str(y) in ['nan', 'NaN', 'Nan'] and df2.iloc[1, x].lower().startswith('втор'):
            df2.iloc[0, x] = 'имеют квалификационную категорию из гр. 5 вторую'
    col_names = dict(zip(df2.columns.tolist(), df2.loc[0, :].values.tolist()))
    df2.drop(index=0, inplace=True)
    df2.rename(columns=col_names, inplace=True)
    df2.rename(columns={re.sub(r'[xls.]', '', z): 'наименование_субъекта'}, inplace=True)
    df2.drop(index=df2[df2['число должностей штатных'].isin(
        ['штатных', 'Штатных', 'Число должностей', 'число должностей'])].index, inplace=True)
    df2.reset_index(drop=True, inplace=True)
    df2[df2.columns[0]] = df2[df2.columns[0]].str.rstrip(r'0123456789. :')
    df2[df2.columns[0]] = df2[df2.columns[0]].replace({'': np.nan})
    df2.dropna(subset=df2.columns[0], inplace=True)
    df2.reset_index(inplace=True, drop=True)
    for x, y in enumerate(df2.columns):
        if y not in [df2.columns[0], 'наименование_субъекта']:
            df2[y] = df2[y].astype(str)
            df2[y] = df2[y].str.replace(',', '.')
            df2[y] = df2[y].astype(float)
    return df2


# формирования службы МК участие в ЧС
def find_df3(df, z):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and y.lower().lstrip().startswith('наименование формиров') and \
                (str(df.loc[x, '2']).lower().startswith('число формир') or
                 str(df.loc[x, '3']).lower().startswith('число формир') or
                 str(df.loc[x, '4']).lower().startswith('число формир')) and len(a) != 1:
            a.append(x)
        if type(y) == str and y.lower().startswith('прочие формиро'):
            a.append(x + 1)
        if len(a) == 2:
            break
    df3 = df[a[0]:a[-1]].copy()
    df3.dropna(axis=1, how='all', inplace=True)
    df3.reset_index(inplace=True, drop=True)
    for x, y in enumerate(df3.loc[0, :]):
        if str(y).lower().startswith('наименование формир') and \
                str(y).lower() != 'наименование_формирований':
            df3.iloc[0, x] = 'наименование_формирований'
        if (str(y) in ['nan', 'NaN', 'Nan'] or str(y).lower().startswith('число формиро')) and \
                df3.iloc[1, x].lower().startswith('всего'):
            df3.iloc[0, x] = 'число_формирований_всего'
        if (str(y) in ['nan', 'NaN', 'Nan'] or str(y).lower().startswith('из них')) and \
                (df3.iloc[1, x].lower().startswith('из них: штат') or df3.iloc[1, x].lower() == 'nan'):
            df3.iloc[0, x] = 'число_формирований_штатных'
        if str(y).lower().startswith('кол-во выездов') and df3.iloc[1, x].lower().startswith('всеми формир'):
            df3.iloc[0, x] = 'Выезды_на_ликвидацию_ЧС_всеми_формированиями'
        if str(y) in ['nan', 'NaN', 'Nan'] and df3.iloc[1, x].lower().startswith('из них штатн'):
            df3.iloc[0, x] = 'Выезды_на_ликвидацию_ЧС_штатными_формированиями'
    col_names = dict(zip(df3.columns.tolist(), df3.loc[0, :].values.tolist()))
    df3.rename(columns=col_names, inplace=True)
    df3.rename(columns={re.sub(r'[xls.]', '', z): 'наименование_субъекта'}, inplace=True)
    df3.drop(index=df3[df3['наименование_формирований'].isin(
        ['Наименование формирований', 'наименование формирований',
         'наименование_формирований'])].index, inplace=True)
    df3[df3.columns[0]] = df3[df3.columns[0]].str.rstrip(r'0123456789. :')
    df3[df3.columns[0]] = df3[df3.columns[0]].replace({'': np.nan})
    df3.dropna(subset=df3.columns[0], inplace=True)
    df3.reset_index(drop=True, inplace=True)
    for x, y in enumerate(df3.columns):
        if y not in ['наименование_формирований', 'наименование_субъекта']:
            df3[y] = df3[y].astype(str)
            df3[y] = df3[y].str.replace(',', '.')
            df3[y] = df3[y].str.extract(r'(\d+)')
            df3[y] = df3[y].astype(float)
    return df3


# пострадавшие в ЧС
def find_df4(df):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and y.lower().lstrip().startswith('наименование чрезвы') and \
                (str(df.loc[x, '2']).lower().startswith('число чс') or
                 str(df.loc[x, '3']).lower().startswith('число чс') or
                 str(df.loc[x, '4']).lower().startswith('число чс')) and len(a) != 1:
            a.append(x)
        if type(y) == str and y.lower().startswith('прочие чс'):
            a.append(x + 1)
        if len(a) == 2:
            break
    df4 = df[a[0]:a[-1]].copy()
    df4.dropna(axis=1, how='all', inplace=True)
    df4.reset_index(inplace=True, drop=True)
    df4[df4.columns[0]] = df4[df4.columns[0]].str.rstrip(r'0123456789. :')
    df4[df4.columns[0]] = df4[df4.columns[0]].replace({'': np.nan})
    for x, y in enumerate(df4['1']):
        if str(y).lower().startswith('наименование чрезвычайных'):
            df4.drop(index=x, inplace=True)
        if str(y).lower().startswith(('(4000)', '\'(4000)', 'продолжение')):
            df4.drop(index=x, inplace=True)
    df4.dropna(subset=['1'], inplace=True)
    df4.reset_index(inplace=True, drop=True)
    df4.rename(columns={
        '1': 'наименование_чрезвычайных_ситуаций',
        '2': 'Число_ЧС_абс',
        '3': 'Число_пострадавших_всего',
        '4': 'Число_пострадавших_детей',
        '5': 'Число_поражённых_всего',
        '6': 'Число_поражённых_детей',
        '7': 'Число_погибших_всего',
        '8': 'Число_погибших_детей',
        '9': 'Количество_крайне_тяжёлых_всего',
        '10': 'Количество_крайне_тяжёлых_детей',
        '11': 'Количество_тяжелых_всего',
        '12': 'Количество_тяжёлых_детей',
        '13': 'Количество_средней_тяжести_всего',
        '14': 'Количество_средней_тяжести_детей',
        '15': 'Количество_лёгкой_тяжести_всего',
        '16': 'Количество_лёгкой_тяжести_детей',
        '17': 'Число_поражённых_которым_оказана_первая_помощь_всего',
        '18': 'Число_поражённых_которым_оказана_первая_помощь_детей'}, inplace=True)
    for x, y in enumerate(df4.columns):
        if y not in ['наименование_чрезвычайных_ситуаций', 'наименование_субъекта']:
            df4[y] = df4[y].astype(str)
            df4[y] = df4[y].str.replace(',', '.')
            df4[y] = df4[y].str.extract(r'(\d+)')
            df4[y] = df4[y].astype(float)
    return df4


# по видам оказанной помощи
def find_df5(df):
    a = []
    for x, y in enumerate(df['1']):
        b = 0
        if type(y) == str and y.lower().lstrip().startswith(r'(4010)'):
            b += 1
        if type(y) == str and y.lower().lstrip().startswith('наименование чрезвы') and \
                (str(df.loc[x, '2']).lower().startswith('число чс') or
                 str(df.loc[x, '3']).lower().startswith('число чс') or
                 str(df.loc[x, '4']).lower().startswith('число чс')) and b > 0 and len(a) > 1:
            a.append(x)
        elif type(y) == str and y.lower().startswith('прочие чс'):
            a.append(x + 1)
        if len(a) == 2:
            break
    df5 = df[a[0]:a[-1]].copy()
    df5.dropna(axis=1, how='all', inplace=True)
    df5.reset_index(inplace=True, drop=True)
    df5[df5.columns[0]] = df5[df5.columns[0]].str.rstrip(r'0123456789. :')
    df5[df5.columns[0]] = df5[df5.columns[0]].replace({'': np.nan})
    for x, y in enumerate(df5['1']):
        if str(y).lower().startswith(('наименование чрезвычайных', '(4010)', '(4000)', 'продолжение')):
            df5.drop(index=x, inplace=True)
    df5.dropna(subset=['1'], inplace=True)
    df5.reset_index(inplace=True, drop=True)
    df5.rename(columns={
        '1': 'наименование_чрезвычайных_ситуаций',
        '2': 'Количество_оказанной_первичной_медикосанитарной_помощи_всего',
        '3': 'Количество_оказанной_первичной_медикосанитарной_помощи_детям',
        '4': 'Количество_оказанной_специализированной_втчВМП_всего',
        '5': 'Количество_оказанной_специализированной_втчВМП_детям',
        '6': 'Количество_оказанной_скоройМП_всего',
        '7': 'Количество_оказанной_скоройМП_детям',
        '8': 'Число_эвакуированных_пораженных_всего',
        '9': 'Число_эвакуированных_пораженных_детей',
        '10': 'Число_госпитализированных_пораженных_всего',
        '11': 'Число_госпитализированных_пораженных_детей',
        '12': 'Число_погибших_доЭвакуации_всего',
        '13': 'Число_погибших_доЭвакуации_детей',
        '14': 'Число_погибших_воВремяЭвакуации_всего',
        '15': 'Число_погибших_воВремяЭвакуации_детей',
        '16': 'Число_погибших_в_медорганизации_всего',
        '17': 'Число_погибших_в_медорганизации_детей'}, inplace=True)
    for x, y in enumerate(df5.columns):
        if y not in ['наименование_чрезвычайных_ситуаций', 'наименование_субъекта']:
            df5[y] = df5[y].astype(str)
            df5[y] = df5[y].str.replace(',', '.')
            df5[y] = df5[y].str.extract(r'(\d+)')
            df5[y] = df5[y].astype(float)
    return df5


# ищем таблицу со сведениями о койках
def find_df6(df):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and y.lower().lstrip().startswith('профиль коек') and \
                (str(df.loc[x, '2']).lower().startswith('число среднегодовых коек') or
                 str(df.loc[x, '3']).lower().startswith('число среднегодовых коек') or
                 str(df.loc[x, '4']).lower().startswith('число среднегодовых коек')):
            a.append(x)
        if type(y) == str and y.lower().startswith('прочие') and \
                str(df.at[x - 1, '1']).lower().startswith('реанимационные'):
            a.append(x + 1)
        if len(a) == 2:
            break
    df6 = df[a[0]:a[-1]].copy()
    df6.dropna(axis=1, how='all', inplace=True)
    df6.reset_index(inplace=True, drop=True)
    df6[df6.columns[0]] = df6[df6.columns[0]].str.rstrip(r'0123456789. :')
    df6[df6.columns[0]] = df6[df6.columns[0]].replace({'': np.nan})
    for x, y in enumerate(df6['1']):
        if str(y).lower().startswith('профиль коек'):
            df6.drop(index=x, inplace=True)
    df6.dropna(subset=['1'], inplace=True)
    df6.reset_index(inplace=True, drop=True)
    df6.rename(columns={
        '1': 'профиль_коек',
        '2': 'Число_среднегодовых_коек_развернутых_вЧС',
        '3': 'Поступило_поражённых_всего',
        '4': 'Поступило_поражённых_детей',
        '5': 'Выписано_поражённых_всего',
        '6': 'Выписано_поражённых_детей',
        '7': 'Умерло_всего',
        '8': 'Умерло_детей',
        '9': 'Проведено_поражёнными_койко_дней'}, inplace=True)

    for x, y in enumerate(df6.columns):
        if y not in ['профиль_коек', 'наименование_субъекта']:
            df6[y] = df6[y].astype(str)
            df6[y] = df6[y].str.replace(',', '.')
            df6[y] = df6[y].astype(float)
    return df6


# сведения об лаборатории психофиз обеспечения ЦМК
def find_df7(df, z):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and y.lower().lstrip().startswith('проведено психофизи') and \
                'Проведена психокоррекция' in df.loc[x, :].values.tolist():
            a.append(x)
        if type(y) == str and y.lower().startswith('проведено освидетель'):
            a.append(x + 5)
        if len(a) == 2:
            break
    if len(a) != 2:
        df7 = pd.DataFrame({0: np.nan, 1: np.nan, 2: np.nan, 3: np.nan, 4: np.nan, 5: np.nan, 6: np.nan,
                            7: np.nan, 8: np.nan, 9: np.nan, 11: np.nan, 12: np.nan, 13: np.nan, 14: np.nan, 15: np.nan,
                            16: np.nan, 17: np.nan, 18: np.nan, 19: np.nan, 20: np.nan, 21: np.nan}, index=[0])
    else:
        df7 = df[a[0]:a[-1] - 5].copy()
        df7_1 = df[a[-1] - 5:a[-1]].copy()
        df7.dropna(axis=1, how='all', inplace=True)
        df7_1.dropna(axis=1, how='all', inplace=True)
        df7.reset_index(drop=True, inplace=True)
        df7_1.reset_index(drop=True, inplace=True)
        a = 0
        for x, y in enumerate(df7_1.values):
            for i, j in enumerate(df7_1.values[x]):
                try:
                    isinstance(int(j), int)
                    a += 1
                    df7_2 = pd.DataFrame(df7_1.loc[x, :]).T
                except:
                    if a > 0:
                        break
                    else:
                        continue
            if a > 0:
                break
        if 'df7_2' not in locals():
            df7_2 = pd.DataFrame(df7_1.loc[0, :]).T
            df7_2.loc[0, :] = np.nan
        df7_2.reset_index(drop=True, inplace=True)
        a = 0
        for x, y in enumerate(df7.values):
            for i, j in enumerate(df7.values[x]):
                try:
                    isinstance(int(j), int)
                    a += 1
                    df7_3 = pd.DataFrame(df7.loc[x, :]).T
                except:
                    if a > 0:
                        break
                    else:
                        continue
            if a > 0:
                break
        if 'df7_3' not in locals():
            df7_3 = pd.DataFrame(df7_1.loc[0, :]).T
            df7_3.loc[0, :] = np.nan
        df7_3.reset_index(drop=True, inplace=True)
        df7 = pd.concat([df7_3, df7_2], axis=1, ignore_index=True)
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
        11: 'Проведено_освидетел_всего',
        12: 'Проведено_освидетел_сотруд_АСФ',
        13: 'Проведено_освидетел_сотруд_СМК',
        14: 'Прошедшие_психреабилитацию_всего',
        15: 'Прошедшие_психреабилитацию_сотруд_АСФ',
        16: 'Прошедшие_психреабилитацию_сотруд_СМК',
        17: 'Прошедшие_психреабилитацию_прочие',
        18: 'Число_психпомощи_населению_в_повседдеятельности',
        19: 'Число_психпомощи_населению_в_ЧС',
        20: 'Число_психпомощи_населению_ТМК_онлайн',
        21: 'наименование_субъекта'}, inplace=True)
    df7.loc[0, 'наименование_субъекта'] = re.sub(r'[xls.]', '', z)
    for x, y in enumerate(df7.columns):
        if df7[y].dtypes == object:
            df7[y] = df7[y].str.replace(',', '.')
        try:
            df7[y] = df7[y].astype(float)
        except:
            continue
    return df7


# сведения об обучении
def find_df8(df, z):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and y.lower().lstrip().startswith('проведено учебных циклов') and \
                'Обучено слушателей' in df.loc[x, :].values.tolist():
            a.append(x)
        if type(y) == str and y.lower().startswith('сведения о проведенных учениях'):
            a.append(x)
        if len(a) == 2:
            break
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
        df8 = df[a[0]:a[-1]].copy()
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
    df8_1.loc[0, 'наименование_субъекта'] = re.sub(r'[xls.]', '', z)
    for x, y in enumerate(df8_1.columns):
        if df8_1[y].dtypes == object:
            df8_1[y] = df8_1[y].str.replace(',', '.')
        try:
            df8_1[y] = df8_1[y].astype(float)
        except:
            continue
    return df8_1


# поиск таблицы учений, занятий, тренировок
def find_df9(df):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and \
                y.lower().lstrip().startswith('наименование чрезвычайной ситуации'):
            a.append(x)
        if type(y) == str and y.lower().startswith('всего') and len(a) > 0:
            a.append(x + 1)
        if len(a) == 2:
            break
    df9 = df[a[0]:a[-1]].copy()
    df9.dropna(axis=1, how='all', inplace=True)
    df9.dropna(axis=0, subset=['1'], inplace=True)
    df9.reset_index(drop=True, inplace=True)
    df9.drop(index=[0], inplace=True)
    df9.reset_index(drop=True, inplace=True)
    df9.rename(columns={
        '1': 'наименование_ЧС',
        '2': 'число_УчТренЗанятий_всего',
        '3': 'число_УчТренЗанятий_КШУ',
        '4': 'число_УчТренЗанятий_ШТ',
        '5': 'число_УчТренЗанятий_ТСУ'}, inplace=True)
    for x, y in enumerate(df9.columns):
        if y not in ['наименование_ЧС', 'наименование_субъекта']:
            df9[y] = df9[y].astype(str)
            df9[y] = df9[y].str.replace(',', '.')
            df9[y] = df9[y].str.extract(r'(\d+)')
            df9[y] = df9[y].astype(float)
    return df9


# поиск таблицы сведений о деятельности трассовых пунктов
def find_df10(df):
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
    return df10


# поиск таблицы сведения о материально-тех оснащении ЦМК
def find_df11(df, z):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and \
                y.lower().lstrip().startswith('автомобильный транспорт всего'):
            a.append(x)
        if type(y) == str and \
                y.lower().startswith('аппарат узи переносной') and \
                len(a) > 0:
            a.append(x + 1)
        if len(a) == 2:
            break
    if len(a) != 2:
        df11 = pd.DataFrame({'1': [
            'Автомобильный транспорт всего',
            'Авиационный транспорт всего',
            'Вертолетные площадки',
            'Средства связи, всего, из них:',
            'Радиостанции',
            'Мобильная связь(сотовые телефоны)',
            'Спутниковые телефоны',
            'Высокоскоростная спутниковая связь'
            'Система мобильных телемедицинских консультаций',
            'Медицинское оборудование, всего, из них:',
            'Электрокардиограф',
            'Эхоэнцефалоскоп',
            'Манипуляционный цистоскоп',
            'Фибробронхоскоп',
            'Аппарат УЗИ переносной'],
            '2': np.nan,
            'наименование_субъекта': re.sub(r'[xls.]', '', z)})
        df11.loc[:, ['1', '2']] = np.nan
    else:
        df11 = df[a[0]:a[-1]].copy()
        df11.dropna(axis=1, how='all', inplace=True)
        df11.reset_index(drop=True, inplace=True)
        if '2' not in df11.columns:
            df11['2'] = np.nan
            df11 = df11[['1', '2', 'наименование_субъекта']]
    df11.rename(columns={
        '1': 'наименование_МТО',
        '2': 'число_единиц'}, inplace=True)
    for x, y in enumerate(df11.columns):
        if df11[y].dtypes == object:
            df11[y] = df11[y].str.replace(',', '.')
        try:
            df11[y] = df11[y].astype(float)
        except:
            continue
    return df11


def find_df56_1(df):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and y.lower().strip() == 'наименование':
            a.append(x)
        if type(y) == str and y.lower().startswith('выездные бригады') and len(a) > 0:
            a.append(x + 1)
        if len(a) == 2:
            break
    df56_1 = df[a[0]:a[-1]].copy()
    df56_1.dropna(axis=1, how='all', inplace=True)
    df56_1.reset_index(drop=True, inplace=True)
    df56_1.drop(index=[0], inplace=True)
    df56_1.reset_index(drop=True, inplace=True)
    df56_1.rename(columns={
        '1': 'наименование_ЧС',
        '2': 'Отметка'}, inplace=True)
    for x, y in enumerate(df56_1.columns):
        if y not in ['наименование_ЧС', 'наименование_субъекта']:
            df56_1[y] = df56_1[y].astype(str)
            df56_1[y] = df56_1[y].str.replace(',', '.')
            df56_1[y] = df56_1[y].astype(float)
    return df56_1


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
        if y not in ['наименование_должностей', 'наименование_субъекта']:
            df56_2[y] = df56_2[y].astype(str)
            df56_2[y] = df56_2[y].str.replace(',', '.')
            df56_2[y] = df56_2[y].astype(float)
    return df56_2


def find_df56_3_2015(df):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and \
                y.lower().strip() == 'наименования':
            a.append(x)
        if type(y) == str and y.lower().startswith('медицинских грузов, тонны') and len(a) > 1:
            a.append('stop')
            a.append(x + 1)
        if 'stop' in a:
            break
    df56_3 = df[a[0]:a[-1]].copy()
    df56_3.dropna(axis=1, how='all', inplace=True)
    df56_3.dropna(axis=0, subset=['1'], inplace=True)
    df56_3.reset_index(drop=True, inplace=True)
    for x, y in enumerate(df56_3['1']):
        if y.lower().strip() == 'наименования':
            df56_3.drop(index=[x], inplace=True)
    df56_3.reset_index(drop=True, inplace=True)
    df56_3.rename(columns={
        '1': 'наименование',
        '2': 'оказана_МП_всего',
        '3': 'оказана_МП_детям',
        '4': 'оказана_МП_ОснРаботниками',
        '5': 'оказанаМПнаДогоспит_всего',
        '6': 'оказанаМПнаДогоспит_детям',
        '7': 'оказанаМПнаДогоспит_ПострадЧС_всего',
        '8': 'оказанаМПнаДогоспит_ПострадЧС_детям',
        '9': 'оказанаМПнаДогоспит_ПострадДТП_всего',
        '10': 'оказанаМПнаДогоспит_ПострадДТП_детям',
        '11': 'оказанаМПвСтационаре_всего',
        '12': 'оказанаМПвСтационаре_детям',
        '13': 'оказанаМПвСтационаре_ПострадЧС_всего',
        '14': 'оказанаМПвСтационаре_ПострадЧС_детям',
        '15': 'оказанаМПвСтационаре_ПострадДТП_всего',
        '16': 'оказанаМПвСтационаре_ПострадДТП_детям'}, inplace=True)
    df56_3['наименование'] = df56_3['наименование'].str.strip()
    for x, y in enumerate(df56_3.columns):
        if y not in ['наименование', 'наименование_субъекта']:
            df56_3[y] = df56_3[y].astype(str)
            df56_3[y] = df56_3[y].str.replace(',', '.')
            df56_3[y] = df56_3[y].str.extract(r'(\d+)')
            df56_3[y] = df56_3[y].astype(float)
    return df56_3


def find_df56_3_no1516(df, z):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and \
                str(y).lower().strip() == 'наименования':
            a.append(x)
        if type(y) == str and str(y).lower().startswith('прочим транспортом,') and len(a) > 1:
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
                (str(df.at[x - 1, '1']).lower().strip().startswith('прочим транспортом,') or
                 str(df.at[x - 2, '1']).lower().strip().startswith('прочим транспортом,') or
                 str(df.at[x - 3, '1']).lower().strip().startswith('прочим транспортом,')):
            a.append(x)
        if type(y) == str and str(y).lower().startswith('прочим транспортом,') and len(a) > 0:
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
    df56_3['наименование_субъекта'] = re.sub(r'[xls.]', '', z)
    return df56_3


def find_df56_3_2016(df, z):
    a = []
    for x, y in enumerate(df['1']):
        if type(y) == str and \
                str(y).lower().strip() == 'наименования':
            a.append(x)
        if type(y) == str and str(y).lower().startswith('медицинских грузов,') and len(a) > 1:
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
                (str(df.at[x - 1, '1']).lower().strip().startswith('медицинских грузов,') or
                 str(df.at[x - 2, '1']).lower().strip().startswith('медицинских грузов,') or
                 str(df.at[x - 3, '1']).lower().strip().startswith('медицинских грузов,')):
            a.append(x)
        if type(y) == str and str(y).lower().startswith('медицинских грузов,') and len(a) > 0:
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
    df56_3['наименование_субъекта'] = re.sub(r'[xls.]', '', z)
    return df56_3


def find_df56_4_1516(df):
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
    df56_4 = df[a[0]:a[-1]].copy()

    df56_4.dropna(axis=1, how='all', inplace=True)
    df56_4.dropna(axis=0, subset=['1'], inplace=True)
    df56_4.reset_index(drop=True, inplace=True)
    df56_4.drop(index=[0], inplace=True)
    df56_4.reset_index(drop=True, inplace=True)
    df56_4.rename(columns={
        '1': 'профили_МП',
        '2': 'оказана_ЭКМП_всего',
        '3': 'оказана_ЭКМП_детям',
        '4': 'оказана_ЭКМП_ПострадЧС_всего',
        '5': 'оказана_ЭКМП_ПострадЧС_детям',
        '6': 'эвакуировано_всего',
        '7': 'эвакуировано_детей',
        '8': 'эвакуировано_ПострадЧС_всего',
        '9': 'эвакуировано_ПострадЧС_детей',
        '10': 'эвакуировано_вРегМО_всего',
        '11': 'эвакуировано_вРегМО_детей',
        '12': 'эвакуировано_вРегМО_ПострадЧС_всего',
        '13': 'эвакуировано_вРегМО_ПострадЧС_детей',
        '14': 'эвакуировано_вМежРегМО_всего',
        '15': 'эвакуировано_вМежРегМО_детей',
        '16': 'эвакуировано_вМежРегМО_ПострадЧС_всего',
        '17': 'эвакуировано_вМежРегМО_ПострадЧС_детей',
        '18': 'эвакуировано_вФедМО_всего',
        '19': 'эвакуировано_вФедМО_детей',
        '20': 'эвакуировано_вФедМО_ПострадЧС_всего',
        '21': 'эвакуировано_вФедМО_ПострадЧС_детей'}, inplace=True)
    df56_4['профили_МП'] = df56_4['профили_МП'].str.strip()
    for x, y in enumerate(df56_4.columns):
        if y not in ['профили_МП', 'наименование_субъекта']:
            df56_4[y] = df56_4[y].astype(str)
            df56_4[y] = df56_4[y].str.replace(',', '.')
            df56_4[y] = df56_4[y].str.extract(r'(\d+)')
            df56_4[y] = df56_4[y].astype(float)
    return df56_4


def find_df56_4_no1516(df):
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
    return df56_4
