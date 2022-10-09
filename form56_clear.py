##
import os
from rename_files import rename_region, fly_yes_llc_group, fly_no_llc_group, no_fly_group
from osnova_clear import choise_paths
import pandas as pd
import re
import numpy as np
from other_function import drop_num, drop_num_2
forma = 55
if forma == 55:
    base_path = choise_paths(forma=55)
    os.chdir(base_path[0] + r'/переработанные_файлы')
    for folder in os.listdir():
        folder_path = os.getcwd()
        os.chdir(folder_path + f'/{folder}')
        dirs = [x for x in os.listdir() if x.endswith(('.xls', '.xlsx'))]
        os.chdir(folder_path + f'/{folder}')
if forma == 56:
    base_path = choise_paths(forma=56)
    os.chdir(base_path[0] + r'/переработанные_файлы')
    for folder in os.listdir():
        folder_path = os.getcwd()
        os.chdir(folder_path + f'/{folder}')
        dirs = [x for x in os.listdir() if x.endswith(('.xls', '.xlsx'))]
        os.chdir(folder_path + f'/{folder}')
##
print(dirs)


