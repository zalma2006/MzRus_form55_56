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
        if df2[y].dtypes == object:
            df2[y] = df2[y].str.replace(',', '.')
            try:
                df2[y] = df2[y].astype(float)
            except:
                continue
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
        if df3[y].dtypes == object:
            df3[y] = df3[y].str.replace(',', '.')
            try:
                df3[y] = df3[y].astype(float)
            except:
                continue
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
        if str(y).lower().startswith('(4000)__'):
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
        if df4[y].dtypes == object:
            df4[y] = df4[y].str.replace(',', '.')
        try:
            df4[y] = df4[y].astype(float)
        except:
            continue
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
        if str(y).lower().startswith('наименование чрезвычайных'):
            df5.drop(index=x, inplace=True)
        if str(y).lower().startswith(r'(4010)__'):
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
        if df5[y].dtypes == object:
            df5[y] = df5[y].str.replace(',', '.')
        try:
            df5[y] = df5[y].astype(float)
        except:
            continue
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
        if df6[y].dtypes == object:
            df6[y] = df6[y].str.replace(',', '.')
        try:
            df6[y] = df6[y].astype(float)
        except:
            continue
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
        1: "Проведен_психофизтест_сотруд_АСФ",
        2: "Проведен_психофизтест_сотруд_СМК",
        3: "Проведен_психофизтест_волонтёров",
        4: "Из_них_годных",
        5: "Из_них_условногодных",
        6: "Проведена_психокоррекция_всего",
        7: "Проведена_психокоррекция_сотруд_АСФ",
        8: "Проведена_психокоррекция_сотруд_СМК",
        9: "Проведена_психокоррекция_волонтёров",
        11: "Проведено_освидетел_всего",
        12: "Проведено_освидетел_сотруд_АСФ",
        13: "Проведено_освидетел_сотруд_СМК",
        14: "Прошедшие_психреабилитацию_всего",
        15: "Прошедшие_психреабилитацию_сотруд_АСФ",
        16: "Прошедшие_психреабилитацию_сотруд_СМК",
        17: "Прошедшие_психреабилитацию_прочие",
        18: "Число_психпомощи_населению_в_повседдеятельности",
        19: "Число_психпомощи_населению_в_ЧС",
        20: "Число_психпомощи_населению_ТМК_онлайн",
        21: "наименование_субъекта"}, inplace=True)
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
        "2": "обучено_всего",
        "3": "обучено_оргздав",
        "4": "обучено_СМП",
        "5": "обучено_МЧС_РФ",
        "6": "обучено_МВД_РФ",
        "7": "обучено_МПС_РФ",
        "8": "обучено_прочие"}, inplace=True)
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
                y.lower().lstrip().startswith('техногенные чс - всего'):
            a.append(x)
        if type(y) == str and y.lower().startswith('всего') and len(a) > 0:
            a.append(x + 1)
        if len(a) == 2:
            break
    df9 = df[a[0]:a[-1]].copy()
    df9.dropna(axis=1, how='all', inplace=True)
    df9.reset_index(drop=True, inplace=True)
    df9.rename(columns={
        "1": "наименование_ЧС",
        "2": "число_УчТренЗанятий_всего",
        "3": "число_УчТренЗанятий_КШУ",
        "4": "число_УчТренЗанятий_ШТ",
        "5": "число_УчТренЗанятий_ТСУ"}, inplace=True)
    for x, y in enumerate(df9.columns):
        if df9[y].dtypes == object:
            df9[y] = df9[y].str.replace(',', '.')
        try:
            df9[y] = df9[y].astype(float)
        except:
            continue
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
        "1": "показатели_о_деят_трасспунктов",
        "2": "число"}, inplace=True)
    for x, y in enumerate(df10.columns):
        if df10[y].dtypes == object:
            df10[y] = df10[y].str.replace(',', '.')
        try:
            df10[y] = df10[y].astype(float)
        except:
            continue
    return df10


# поиск таблицы сведения о материально-тех оснащении ЦМК
def find_df11(df):
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
    df11 = df[a[0]:a[-1]].copy()
    df11.dropna(axis=1, how='all', inplace=True)
    df11.reset_index(drop=True, inplace=True)
    if '2' not in df11.columns:
        df11['2'] = np.nan
        df11 = df11[['1', '2', 'наименование_субъекта']]
    df11.rename(columns={
        "1": "наименование_МТО",
        "2": "число_единиц"}, inplace=True)
    for x, y in enumerate(df11.columns):
        if df11[y].dtypes == object:
            df11[y] = df11[y].str.replace(',', '.')
        try:
            df11[y] = df11[y].astype(float)
        except:
            continue
    return df11
