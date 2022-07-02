import os
base_path = r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)'
papki = os.listdir(base_path)
# создадим папки для работы
for x, y in enumerate(papki):
    os.chdir(base_path + f'/{y}')
    if 'ФОРМА 55' in os.listdir():
        os.chdir(os.getcwd() + r'/ФОРМА 55')
    if 'для программы' in os.listdir():
        os.chdir(os.getcwd() + r'/для программы')
    else:
        os.mkdir(os.getcwd() + r'/для программы')
        os.chdir(os.getcwd() + r'/для программы')
    if 'переработанные файлы' in os.listdir():
        os.chdir(os.getcwd() + r'/переработанные файлы')
    else:
        os.mkdir(os.getcwd() + r'/переработанные файлы')
        os.chdir(os.getcwd() + r'/переработанные файлы')
    if 'Табл_сведения_о_центре_МК1' in os.listdir():
        os.chdir(os.getcwd() + r'/Табл_сведения_о_центре_МК')
    else:
        os.mkdir(os.getcwd() + r'/Табл_сведения_о_центре_МК')
        os.mkdir(os.getcwd() + r'/Сведения_о_кадрах_мк')
        os.mkdir(os.getcwd() + r'/Формирования_мк')
        os.mkdir(os.getcwd() + r'/Сведения_о_пострадавших_ЧС')
        os.mkdir(os.getcwd() + r'/Сведения_о_видах_помощи_вЧС')
        os.mkdir(os.getcwd() + r'/Использование_КФ_приЧС')
        os.mkdir(os.getcwd() + r'/Сведения_о_лаборатории_мк')
        os.mkdir(os.getcwd() + r'/Сведения_о_обучении')
        os.mkdir(os.getcwd() + r'/Сведения_о_учениях_трениров_занят')
        os.mkdir(os.getcwd() + r'/Сведения_о_трассовых_пунктах')
        os.mkdir(os.getcwd() + r'/Сведения_о_МТО_МК')
