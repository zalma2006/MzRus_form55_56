import os
import pandas as pd
import re


class Move:
    """
    Класс Move отвечает за обход папок и файлов сбор полных путей до файлов/папок
    lists_dir - заходит в папку указанного пути объекта получает все вложенные папки и
    выводит список полных путей до вложенных папок
    lists_file - заходит в папку указанного пути объекта получает все вложенные файлы и
    выводит список полных путей до вложенных файлов
    remove_dir - изменяет рабочий каталог до верхнего каталога
    """

    def __init__(self, path: str):
        self.path = path
        self.list_dir = None
        self.list_file = None
        self.paths = None

    def lists_dir(self):
        os.chdir(self.path)
        list_dir = os.listdir()
        self.list_dir = [os.getcwd() + f'/{_}' for _ in list_dir if os.path.isdir(os.getcwd() + f'/{_}')]
        return self.list_dir

    def lists_file(self):
        os.chdir(self.path)
        list_file = os.listdir()
        self.list_file = [os.getcwd() + f'/{_}' for _ in list_file if os.path.isfile(os.getcwd() + f'/{_}')]
        return self.list_file

    def remove_dir(self):
        os.chdir(os.path.split(self.path)[0])


class Grouper:
    """
    Класс определяет работу со сводными таблицами
    Несколько функций
    forms - отвечает за определение учётно-отчётной формы объекта - 55 или 56
    forma_56 - отвечает за определение с шаблона формы
    forma_56_1/2../и т д - отвечает за правильную группировку формы и её сохранение
    delete - отвечает за удаление сводных таблиц
    save_file - отвечает за реиндексацию и сохранения сводной таблицы
    """

    def __init__(self, path, df):
        self.path: str = path
        self.df = df
        self.form: str = self.path.split('/')[-2]
        self.groups: str = self.path.split('/')[-1]
        self.forma: int = int([x for x in self.path.split('/') if str(x).endswith((' 56', ' 55'))][0][-2:])
        self.years: tuple = ('2015', '2016', '2017', '2018', '2019', '2020')
        self.year: str = re.match('(\d+)', [x for x in self.path.split('/') if str(x).startswith(self.years)][0])[0]
        self.full_path_group: str = self.path + f'/{self.form}_свод_{self.groups}_{self.year}.xlsx'
        self.full_path_all: str = self.path + f'/{self.form}_свод_{self.groups}_{self.year}_полный.xlsx'
        self.__agg_dict = None
        self.__agg_list2 = None
        self.__agg_list1 = None
        self.base_path = '/home/maks/Документы/Ирина/диссертация/формы_мз_55_56/сводные_таблицы'
        self.path_save_group = self.base_path + '/сводные_по_группам_все_года' + \
                               f'/{self.form}_свод_{self.groups}_{self.year}.xlsx'
        self.path_save_all = self.base_path + '/полные_по_группам_все_года' + \
                             f'/{self.form}_свод_{self.groups}_{self.year}_полный.xlsx'
        self.base_path_1 = '/home/maks/Документы/Ирина/диссертация/формы_мз_55_56/сводные_таблицы/полные_по_группам_' \
                           'все_года'
        self.base_path_2 = '/home/maks/Документы/Ирина/диссертация/формы_мз_55_56/сводные_таблицы'

    def agg_dict(self):
        # создаём словарь аггрегаций по столбцам, исключаем строковые столбцы и столбец с указанием отчетного года
        self.__agg_list1: list = [x for x in self.df.columns if self.df[x].dtypes != object and str(x) != 'год']
        self.__agg_list2: list = list(map(lambda x: 'sum', range(len(self.__agg_list1))))
        self.__agg_dict: dict = dict(zip(self.__agg_list1, self.__agg_list2))
        self.__agg_dict['год'] = 'min'
        return self.__agg_dict

    def save_file(self):
        self.df = self.df.reset_index(drop=False)
        self.df.to_excel(self.full_path_group, index=False)
        path_file = os.path.dirname(self.path_save_group)
        if os.path.isdir(path_file):
            self.df.to_excel(self.path_save_group, index=False)
        else:
            os.mkdir(path_file)
            self.df.to_excel(self.path_save_group, index=False)

    def save_file_all_row(self):
        self.df.to_excel(self.full_path_all, index=False)
        path_file = os.path.dirname(self.path_save_all)
        if os.path.isdir(path_file):
            self.df.to_excel(self.path_save_all, index=False)
        else:
            os.mkdir(path_file)
            self.df.to_excel(self.path_save_all, index=False)

    def forms(self):
        self.__agg_dict = self.agg_dict()
        if self.forma == 56:
            self.forma_56()
        if self.forma == 55:
            self.forma_55()

    def forma_56(self):
        self.save_file_all_row()
        if str(self.form).startswith('Сведения_отдЭКМПиМЭ'):
            self.forma_56_1()
        if str(self.form).startswith('Кадры_отдЭКМПиМЭ'):
            self.forma_56_2()
        if str(self.form).startswith('Деятельность_отдЭКМПиМЭ'):
            self.forma_56_3()
        if str(self.form).startswith('Выезды_отдЭКМПиМЭ'):
            self.forma_56_4()
        self.save_file()

    def forma_56_1(self):
        self.df = self.df.groupby(by=['наименование']).aggregate(self.__agg_dict)

    def forma_56_2(self):
        self.df = self.df.groupby(by=['наименование_должностей']).aggregate(self.__agg_dict)

    def forma_56_3(self):
        self.df = self.df.groupby(by=['наименование']).aggregate(self.__agg_dict)

    def forma_56_4(self):
        self.df = self.df.groupby(by=['профили_МП']).aggregate(self.__agg_dict)

    def forma_55(self):
        self.save_file_all_row()
        if str(self.form).startswith('Табл_сведения_о_центре_МК'):
            self.forma55_1()
        if str(self.form).startswith('Сведения_о_кадрах_мк'):
            self.forma55_2()
        if str(self.form).startswith('Формирования_мк'):
            self.forma55_3()
        if str(self.form).startswith('Сведения_о_пострадавших_ЧС'):
            self.forma55_4()
        if str(self.form).startswith('Сведения_о_видах_помощи_вЧС'):
            self.forma55_5()
        if str(self.form).startswith('Использование_КФ_приЧС'):
            self.forma55_6()
        if str(self.form).startswith('Сведения_о_лаборатории_мк'):
            self.forma55_7()
        if str(self.form).startswith('Сведения_о_обучении'):
            self.forma55_8()
        if str(self.form).startswith('Сведения_о_учениях_трениров_занят'):
            self.forma55_9()
        if str(self.form).startswith('Сведения_о_трассовых_пунктах'):
            self.forma55_10()
        if str(self.form).startswith('Сведения_о_МТО_МК'):
            self.forma55_11()

    def forma55_1(self):
        self.df = self.df.groupby(by=['наименование']).aggregate(self.__agg_dict)
        self.save_file()

    def forma55_2(self):
        self.df = self.df.groupby(by=['наименование_должностей']).aggregate(self.__agg_dict)
        self.save_file()

    def forma55_3(self):
        self.df = self.df.groupby(by=['наименование_формирований']).aggregate(self.__agg_dict)
        self.save_file()

    def forma55_4(self):
        self.df = self.df.groupby(by=['наименование_чрезвычайных_ситуаций']).aggregate(self.__agg_dict)
        self.save_file()

    def forma55_5(self):
        self.df = self.df.groupby(by=['наименование_чрезвычайных_ситуаций']).aggregate(self.__agg_dict)
        self.save_file()

    def forma55_6(self):
        self.df = self.df.groupby(by=['профиль_коек']).aggregate(self.__agg_dict)
        self.save_file()

    def forma55_7(self):
        self.save_file()

    def forma55_8(self):
        self.save_file()

    def forma55_9(self):
        self.df = self.df.groupby(by=['наименование_Чс']).aggregate(self.__agg_dict)
        self.save_file()

    def forma55_10(self):
        self.df = self.df.groupby(by=['показатели_о_деят_трасспунктов']).aggregate(self.__agg_dict)
        self.save_file()

    def forma55_11(self):
        self.df = self.df.groupby(by=['наименование_МТО']).aggregate(self.__agg_dict)
        self.save_file()

    def delete_file(self):
        try:
            os.remove(self.full_path_all)
        except FileNotFoundError:
            print(f'Файл {self.full_path_all} не удален')
        try:
            os.remove(self.full_path_group)
        except FileNotFoundError:
            print(f'Файл {self.full_path_group} не удален')
        try:
            os.remove(self.path_save_group)
        except FileNotFoundError:
            print(f'Файл {self.path_save_group} не удален')
        try:
            os.remove(self.path_save_all)
        except FileNotFoundError:
            print(f'Файл {self.path_save_all} не удален')

    def create_svod_forms(self):
        files = [x for x in os.listdir(self.base_path_1) if os.path.isfile(self.base_path_1 + f'/{x}')]
        forms = list(set([x.split('_свод_')[0] for x in files]))
        raspred = {}
        for i in forms:
            raspred[i] = [self.base_path_1 + f'/{x}' for x in os.listdir(self.base_path_1) if x.startswith(i)]
        for key, val in raspred.items():
            df = pd.DataFrame()
            for x in val:
                df1 = pd.read_excel(x, engine='openpyxl')
                group = x.split('/')[-1]
                group = int(''.join(re.findall('группа_(\d)_', group)))
                cols = df1.columns.tolist()
                cols.remove('наименование_субъекта')
                cols.insert(0, 'наименование_субъекта')
                df1 = df1[cols].copy()
                df1['группа'] = group
                df = pd.concat([df, df1], ignore_index=True)
            col = df.columns[1]
            df.sort_values(by=['год', 'наименование_субъекта', col, 'группа'], ignore_index=True, inplace=True)
            df.to_excel(self.base_path_2 + f'/{key}_{self.base_path_1.split("/")[-1]}.xlsx', index=False)

    def delete_dop_files(self):
        for _ in os.listdir(self.base_path_2):
            if os.path.isfile(self.base_path_2 + f'/{_}'):
                try:
                    os.remove(self.base_path_2 + f'/{_}')
                except FileNotFoundError:
                    print(f'Файл {self.base_path_2 + f"/{_}"} не удален')
            elif os.path.isdir(self.base_path_2 + f'/{_}'):
                try:
                    os.remove(self.base_path_2 + f'/{_}')
                except NotADirectoryError or IsADirectoryError:
                    print(f'Папка {self.base_path_2 + f"/{_}"} не удалена')


def create_end_svod():
    # создаём окончательные сводные таблицы по регионам за все года

    years = ('2015', '2016', '2017', '2018', '2019', '2020')

    path = '/home/maks/Документы/Ирина/диссертация/формы_мз_55_56/сводные_таблицы'
    files = [x for x in os.listdir(path) if os.path.isfile(path + f'/{x}')]

    def data_region(path: str):
        return pd.read_excel(path, engine='openpyxl')

    df = data_region('/home/maks/Документы/Ирина/диссертация/формы_мз_55_56/Численность и смертность вместе 2015-20'
                     '20.xlsx')
    df.rename(columns={'Название_региона': 'наименование_субъекта'}, inplace=True)
    folder_list_55 = ['Табл_сведения_о_центре_МК', 'Сведения_о_кадрах_мк', 'Формирования_мк',
                      'Сведения_о_пострадавших_ЧС', 'Сведения_о_видах_помощи_вЧС', 'Использование_КФ_приЧС',
                      'Сведения_о_лаборатории_мк', 'Сведения_о_обучении',
                      'Сведения_о_учениях_трениров_занят',
                      'Сведения_о_трассовых_пунктах', 'Сведения_о_МТО_МК']
    folder_list_56 = ['Сведения_отдЭКМПиМЭ', 'Кадры_отдЭКМПиМЭ', 'Деятельность_отдЭКМПиМЭ', 'Выезды_отдЭКМПиМЭ']

    df2 = pd.DataFrame()
    for col_year in years:
        year = int(col_year)
        cols_year = [df.columns[0]] + [x for x in df.columns if x[-4:].endswith(col_year)]
        df['год'] = year
        cols_year.append('год')
        df1 = df[cols_year].copy()
        cols_year = ['_'.join(x.split('_')[:-1]) for x in df1.columns if x not in ['год', 'наименование_субъекта']]
        cols_year.insert(0, 'наименование_субъекта')
        cols_year.append('год')
        rename_cols = dict(zip(df1.columns.tolist(), cols_year))
        df1.rename(columns=rename_cols, inplace=True)
        df2 = pd.concat([df2, df1], ignore_index=True)

    for file in files:
        df = data_region(path + f'/{file}')
        for _ in folder_list_55:
            if file.startswith(_):
                forma = 'форма_55_'
        for _ in folder_list_56:
            if file.startswith(_):
                forma = 'форма_56_'
        if forma is None:
            print('Что то пошло не так, не определена форма')
        df = df.merge(df2, how='left', left_on=['наименование_субъекта', 'год'],
                      right_on=['наименование_субъекта', 'год'])
        df.to_excel(path + f'/{forma}{file}', index=False)
        try:
            os.remove(path + f'/{file}')
        except FileNotFoundError:
            print(f'Файл {path + f"/{file}"} не найден!')
        print(f' Сводная таблица {forma}{file} готова!')


def create_del_svod_groups(base_path: str):
    # функция создания сводных таблиц
    print('-' * 57)
    print('Введите 1 если хотите добавить сводные таблицы по группам')
    print('Введите 2 если хотите удалить сводные таблицы по группам')
    print('Введите 3 если хотите выйти')
    print('-' * 57)
    choise_1 = int(input('Введите сюда число: '))
    path_1 = Move(base_path)

    if choise_1 != 3:

        for _ in path_1.lists_dir():
            path_2 = Move(_)
            for _ in path_2.lists_dir():
                path_3 = Move(_)
                for _ in path_3.lists_dir():
                    path_4 = Move(_)
                    for _ in path_4.lists_dir():
                        path_5 = Move(_)
                        for _ in path_5.lists_dir():
                            path_6 = Move(_)
                            for _ in path_6.lists_dir():
                                path_7 = Move(_)
                                df = pd.DataFrame()
                                use_file = [x for x in path_7.lists_file() if not str(x).split('/')[-1].startswith(
                                    path_7.lists_file()[0].split('/')[-3])]
                                if len(use_file) > 1:
                                    for file in use_file:
                                        df1 = pd.read_excel(file)
                                        df = pd.concat([df, df1], ignore_index=True)
                                    svod = Grouper(os.path.split(file)[0], df)
                                    if choise_1 == 1:
                                        svod.forms()
                                    elif choise_1 == 2:
                                        svod.delete_file()
                                    print(f'Год: {svod.year} | Форма: {svod.forma} | {svod.form} | {svod.groups} | '
                                          f'Размер сводной таблицы: {svod.df.shape}')
                                else:
                                    continue
        if choise_1 == 1:
            svod.create_svod_forms()
            create_end_svod()
        elif choise_1 == 2:
            svod.delete_dop_files()
    else:
        pass
