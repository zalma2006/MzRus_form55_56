import os
import re
import warnings
from create_folders import del_folder, create_folder
from other_function import clear_df

warnings.filterwarnings('ignore')
DEBUG = True


def choise_work():
    while True:
        pr_str_1 = 'Введите 1 если хотите обновить выгрузку данных 55 формы'
        pr_str_2 = 'Введите 2 если хотите обновить выгрузку данных 56 формы'
        pr_str_3 = 'Введите 3 если хотите удалить файлы 55 формы'
        pr_str_4 = 'Введите 4 если хотите удалить файлы 56 формы'
        pr_str_5 = 'Введите 5 если хотите создать папки для 55 формы'
        pr_str_6 = 'Введите 6 если хотите создать папки для 56 формы'
        pr_str_7 = 'Введите 7 если хотите перенести файлы по группам'
        pr_str_8 = 'Введите 8 если хотите выйти из программы'

        print('-' * 60)
        print(f'{pr_str_1:>60}')
        print(f'{pr_str_2:>60}')
        print(f'{pr_str_3:>60}')
        print(f'{pr_str_4:>60}')
        print(f'{pr_str_5:>60}')
        print(f'{pr_str_6:>60}')
        print(f'{pr_str_7:>60}')
        print(f'{pr_str_8:>60}')
        print('-' * 60)
        choise = int(input())
        if choise == 1:
            forma = 55
            base_path = choise_paths(forma=forma)
            problems = {}
            for path in base_path:
                year = ''.join(re.findall(r'\d+', path.split(r'/')[-3]))
                problems[year] = clear_df(base_path=path, forma=forma, problems=problems)
            os.chdir(r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56')
            with open('problems_form55.txt', 'w') as f:
                for key, val in problems.items():
                    f.write(f'{key}: {val}\n')
            print(problems)
            break
        elif choise == 2:
            forma = 56
            base_path = choise_paths(forma=forma)
            problems = {}
            for path in base_path:
                year = ''.join(re.findall(r'\d+', path.split(r'/')[-3]))
                problems[year] = clear_df(base_path=path, forma=forma, problems=problems)
            os.chdir(r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56')
            with open('problems_form56.txt', 'w') as f:
                for year, problem in problems.items():
                    f.write(f'{year}: {problem}\n')
            print(problems)
            break
        elif choise == 3:
            forma = r'/ФОРМА 55'
            papka_files1 = 'для_программы'
            papka_files2 = 'переработанные_файлы'
            base_path = r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56'
            del_folder(base_path=base_path, form=forma, papka_files1=papka_files1,
                       papka_files2=papka_files2)
            break
        elif choise == 4:
            forma = r'/ФОРМА 56'
            papka_files1 = 'для_программы'
            papka_files2 = 'переработанные_файлы'
            base_path = r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56'
            del_folder(base_path=base_path, form=forma, papka_files1=papka_files1,
                       papka_files2=papka_files2)
            break
        elif choise == 5:
            base_path = '/media/maks/общее/Ирина/диссертация/формы_мз_55_56'
            folder_list = [r'/Табл_сведения_о_центре_МК', r'/Сведения_о_кадрах_мк', r'/Формирования_мк',
                           r'/Сведения_о_пострадавших_ЧС', r'/Сведения_о_видах_помощи_вЧС', r'/Использование_КФ_приЧС',
                           r'/Сведения_о_лаборатории_мк', r'/Сведения_о_обучении',
                           r'/Сведения_о_учениях_трениров_занят',
                           r'/Сведения_о_трассовых_пунктах', r'/Сведения_о_МТО_МК']
            form = r'/ФОРМА 55'
            papka_files1 = 'для_программы'
            papka_files2 = 'переработанные_файлы'
            create_folder(base_path=base_path, folder_list=folder_list, form=form, papka_files1=papka_files1,
                          papka_files2=papka_files2)
            break
        elif choise == 6:
            base_path = '/media/maks/общее/Ирина/диссертация/формы_мз_55_56'
            folder_list = [r'/Сведения_отдЭКМПиМЭ', r'/Кадры_отдЭКМПиМЭ',
                           r'/Деятельность_отдЭКМПиМЭ', r'/Выезды_отдЭКМПиМЭ']
            form = r'/ФОРМА 56'
            papka_files1 = 'для_программы'
            papka_files2 = 'переработанные_файлы'
            create_folder(base_path=base_path, folder_list=folder_list, form=form, papka_files1=papka_files1,
                          papka_files2=papka_files2)
            break
        elif choise == 7:
            from move_files import move_dir, base_path
            from rename_files import fly_yes_llc_group, fly_no_llc_group, no_fly_group
            import shutil
            error_dict = move_dir(base_path=base_path)
            choise_error = int(input('Введите 1 если хотите ли вы посмотреть словарь с ошибками: '))
            if choise_error == 1:
                print(error_dict)
            else:
                break
        elif choise == 8:
            break
        else:
            print('Вы не выбрали действие!')


def choise_paths(forma):
    if forma == 55:
        base_path = [r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2015 г/ФОРМА 55/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2016 г/ФОРМА 55/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2017 г/ФОРМА 55/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2018 г/ФОРМА 55/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2019 г/ФОРМА 55/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2020 г/ФОРМА 55/для_программы']
        return base_path
    if forma == 56:
        base_path = [r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2015 г/ФОРМА 56/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2016 г/ФОРМА 56/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2017 г/ФОРМА 56/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2018 г/ФОРМА 56/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2019 г/ФОРМА 56/для_программы',
                     r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56/2020 г/ФОРМА 56/для_программы']
        return base_path


choise_work()
