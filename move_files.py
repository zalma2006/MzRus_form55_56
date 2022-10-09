import os
import shutil
from rename_files import fly_yes_llc_group, fly_no_llc_group, no_fly_group

base_path = r'/media/maks/общее/Ирина/диссертация/формы_мз_55_56'


def move_dir(base_path):
    paths_file = []
    error_dict = {}
    for folder in os.listdir(base_path):
        if os.path.isdir(base_path + f'/{folder}'):
            os.chdir(f'{base_path}/{folder}')
            for fol_1 in os.listdir(os.getcwd()):
                if os.path.isdir(os.getcwd() + f'/{fol_1}'):
                    os.chdir(os.getcwd() + f'/{fol_1}')
                    tmp_fol = list(set(os.listdir(os.getcwd())))
                    for name_fol_2 in tmp_fol:
                        if name_fol_2.lower().__contains__('программ'):
                            os.chdir(os.getcwd() + f'/{name_fol_2}')
                            break
                    for name_fol_3 in os.listdir(os.getcwd()):
                        if name_fol_3.lower().__contains__('переработанны'):
                            os.chdir(os.getcwd() + f'/{name_fol_3}')
                            break
                    base_path_1 = os.getcwd()
                    for tmp_fol_1 in os.listdir(os.getcwd()):
                        os.chdir(os.getcwd() + f'/{tmp_fol_1}')
                        base_path_2 = os.getcwd()
                        for fol_4 in os.listdir(os.getcwd()):
                            group_list = ['группа_1', 'группа_2', 'группа_3']
                            if os.path.isfile(os.getcwd() + f'/{fol_4}'):
                                for name in fly_no_llc_group:
                                    if fol_4.lower().__contains__(name):
                                        shutil.move(os.getcwd() + f'/{fol_4}',
                                                    os.getcwd() + f'/{group_list[0]}/{fol_4}')
                                        if fol_4 not in os.listdir(os.getcwd() + f'/{group_list[0]}'):
                                            error_dict[fol_4] = f'Файл не перенесён {os.getcwd()}'
                                            break
                                for name in fly_yes_llc_group:
                                    if fol_4.lower().__contains__(name):
                                        shutil.move(os.getcwd() + f'/{fol_4}',
                                                    os.getcwd() + f'/{group_list[1]}/{fol_4}')
                                        if fol_4 not in os.listdir(os.getcwd() + f'/{group_list[0]}'):
                                            error_dict[fol_4] = f'Файл не перенесён {os.getcwd()}'
                                            break
                                for name in no_fly_group:
                                    if fol_4.lower().__contains__(name):
                                        shutil.move(os.getcwd() + f'/{fol_4}',
                                                    os.getcwd() + f'/{group_list[2]}/{fol_4}')
                                        if fol_4 not in os.listdir(os.getcwd() + f'/{group_list[0]}'):
                                            error_dict[fol_4] = f'Файл не перенесён {os.getcwd()}'
                                            break
                                os.chdir(f'{base_path_2}')
                        os.chdir(f'{base_path_1}')
                os.chdir(f'{base_path}/{folder}')
        os.chdir(base_path)

    return error_dict


error_dict = move_dir(base_path=base_path)



