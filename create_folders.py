import os
import shutil

folder = 55
if folder == 56:
    folder_list = ['Сведения_отдЭКМПиМЭ', 'Кадры_отдЭКМПиМЭ', 'Деятельность_отдЭКМПиМЭ', 'Выезды_отдЭКМПиМЭ']
    form = r'/ФОРМА 56'
    papka_files1 = 'для_программы'
    papka_files2 = 'переработанные_файлы'
if folder == 55:
    folder_list = [r'/Табл_сведения_о_центре_МК', r'/Сведения_о_кадрах_мк', r'/Формирования_мк',
                   r'/Сведения_о_пострадавших_ЧС', r'/Сведения_о_видах_помощи_вЧС', r'/Использование_КФ_приЧС',
                   r'/Сведения_о_лаборатории_мк', r'/Сведения_о_обучении', r'/Сведения_о_учениях_трениров_занят',
                   r'/Сведения_о_трассовых_пунктах', r'/Сведения_о_МТО_МК']
    form = r'/ФОРМА 55'
    papka_files1 = 'для программы'
    papka_files2 = 'переработанные файлы'
else:
    pass
base_path = r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)'


# создадим папки для работы
def create_folder(base_path, form, papka_files1, papka_files2, folder_list):
    papki = os.listdir(base_path)
    for x, y in enumerate(papki):
        if os.path.isdir(base_path + f'/{y}'):
            os.chdir(base_path + f'/{y}' + form)
            if form in os.listdir():
                os.chdir(os.getcwd() + form)
            if papka_files1 in os.listdir():
                os.chdir(os.getcwd() + f'/{papka_files1}')
            else:
                os.mkdir(os.getcwd() + f'/{papka_files1}')
                os.chdir(os.getcwd() + f'/{papka_files1}')
            if papka_files2 in os.listdir():
                os.chdir(os.getcwd() + f'/{papka_files2}')
            else:
                os.mkdir(os.getcwd() + f'/{papka_files2}')
                os.chdir(os.getcwd() + f'/{papka_files2}')
            for i, j in enumerate(folder_list):
                os.mkdir(os.getcwd() + f'/{j}')




def del_folder(base_path, form, papka_files1, papka_files2):
    papki = os.listdir(base_path)
    for x, y in enumerate(papki):
        if os.path.isdir(base_path + f'/{y}'):
            os.chdir(base_path + f'/{y}' + form)
            if form in os.listdir():
                os.chdir(os.getcwd() + form)
            if papka_files1 in os.listdir():
                os.chdir(os.getcwd() + f'/{papka_files1}')
            else:
                continue
            if papka_files2 in os.listdir():
                shutil.rmtree(os.getcwd() + f'/{papka_files2}')
            else:
                continue

def create_or_del():
    while True:
        choise = int(input('Введите 1 если хотите создать папки для файлов, или 2 если хотите удалить папки '
                           'с файлами '))
        if choise == 1:
            create_folder(base_path=base_path, form=form, papka_files1=papka_files1,
                          papka_files2=papka_files2, folder_list=folder_list)
            break
        elif choise == 2:
            del_folder(base_path=base_path, form=form, papka_files1=papka_files1, papka_files2=papka_files2)
            break
        else:
            print('Вы не выбрали действие')

create_or_del()
