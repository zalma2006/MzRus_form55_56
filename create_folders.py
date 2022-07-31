import os
import shutil


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
                if j[1:] in os.listdir(os.getcwd()):
                    os.chdir(os.getcwd() + f'{j}')
                    group_path = os.getcwd()
                    os.mkdir(group_path + r'/группа_1')
                    os.mkdir(group_path + r'/группа_2')
                    os.mkdir(group_path + r'/группа_3')
                    os.chdir(base_path + f'/{y}' + form + f'/{papka_files1}' + f'/{papka_files2}')
                else:
                    os.mkdir(os.getcwd() + f'{j}')
                    os.chdir(os.getcwd() + f'{j}')
                    group_path = os.getcwd()
                    os.mkdir(group_path + r'/группа_1')
                    os.mkdir(group_path + r'/группа_2')
                    os.mkdir(group_path + r'/группа_3')
                    os.chdir(base_path + f'/{y}' + form + f'/{papka_files1}' + f'/{papka_files2}')


def del_folder(base_path, form, papka_files1, papka_files2):
    papki = os.listdir(base_path)
    for x, y in enumerate(papki):
        if os.path.isdir(base_path + f'/{y}'):
            os.chdir(base_path + f'/{y}' + form)
            if form[:1] in os.listdir():
                os.chdir(os.getcwd() + form)
            if papka_files1 in os.listdir():
                os.chdir(os.getcwd() + f'/{papka_files1}')
            else:
                continue
            if papka_files2 in os.listdir():
                shutil.rmtree(os.getcwd() + f'/{papka_files2}')
            else:
                continue


# def create_or_del():
#     while True:
#         choise = int(input('Введите 1 если хотите создать папки для файлов, или 2 если хотите удалить папки '
#                            'с файлами '))
#         if choise == 1:
#             create_folder(base_path=base_path, form=form, papka_files1=papka_files1,
#                           papka_files2=papka_files2, folder_list=folder_list)
#             break
#         elif choise == 2:
#             del_folder(base_path=base_path, form=form, papka_files1=papka_files1, papka_files2=papka_files2)
#             break
#         else:
#             print('Вы не выбрали действие')
