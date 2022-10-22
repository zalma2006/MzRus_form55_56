##
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
        self.form: str = self.path.split('/')[-2]
        self.groups: str = self.path.split('/')[-1]
        self.forma: int = int([x for x in self.path.split('/') if str(x).endswith((' 56', ' 55'))][0][-2:])
        self.years: tuple = ('2015', '2016', '2017', '2018', '2019', '2020')
        self.year: str = re.match('(\d+)', [x for x in self.path.split('/') if str(x).startswith(self.years)][0])[0]
        self.full_path_group: str = self.path + f'/{self.form}_свод_{self.groups}_{self.year}.xlsx'
        self.df = df
        self.__agg_dict = None
        self.__agg_list2 = None
        self.__agg_list1 = None

    def agg_dict(self):
        self.__agg_list1: list = [x for x in self.df.columns if self.df[x].dtypes != object and str(x) != 'год']
        self.__agg_list2: list = list(map(lambda x: 'sum', range(len(self.__agg_list1))))
        self.__agg_dict: dict = dict(zip(self.__agg_list1, self.__agg_list2))
        self.__agg_dict['год'] = 'min'
        return self.__agg_dict

    def save_file(self):
        self.df = self.df.reset_index(drop=False)
        self.df.to_excel(self.full_path_group, index=False)

    def forms(self):
        if self.forma == 56:
            self.forma_56()
        elif self.forma == 55:
            pass
            # self.forma_55()

    def forma_56(self):
        if str(self.form).startswith('Сведения_отдЭКМПиМЭ'):
            self.forma_56_1()
        if str(self.form).startswith('Кадры_отдЭКМПиМЭ'):
            self.forma_56_2()
        if str(self.form).startswith('Деятельность_отдЭКМПиМЭ'):
            self.forma_56_3()
        if str(self.form).startswith('Выезды_отдЭКМПиМЭ'):
            self.forma_56_4()

    def forma_56_1(self):
        self.df = self.df.groupby(by=self.df.columns[0]).agg({self.df.columns[1]: 'sum',
                                                              self.df.columns[-1]: 'min'})
        self.save_file()

    def forma_56_2(self):
        self.__agg_dict = self.agg_dict()
        self.df = self.df.groupby(by=['наименование_должностей']).aggregate(self.__agg_dict)
        self.save_file()

    def forma_56_3(self):
        self.__agg_dict = self.agg_dict()
        self.df = self.df.groupby(by=['наименование']).aggregate(self.__agg_dict)
        self.save_file()

    def forma_56_4(self):
        self.__agg_dict = self.agg_dict()
        self.df = self.df.groupby(by=['профили_МП']).aggregate(self.__agg_dict)
        self.save_file()

    def delete_file(self):
        try:
            os.remove(self.full_path_group)
        except FileNotFoundError:
            pass


base_path = '/home/maks/Документы/Ирина/диссертация/формы_мз_55_56'


def create_del_svod_groups(base_path):
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
                                for file in path_7.lists_file():
                                    df1 = pd.read_excel(file)
                                    df = pd.concat([df, df1], ignore_index=True)
                                svod = Grouper(os.path.split(file)[0], df)
                                if choise_1 == 1:
                                    svod.forms()
                                elif choise_1 == 2:
                                    svod.delete_file()
                                print(f'Год: {svod.year} | Форма: {svod.forma} | {svod.form} ||| '
                                      f'Размер сводной таблицы: {svod.df.shape}')

    else:
        pass


