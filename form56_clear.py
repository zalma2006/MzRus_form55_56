##
import os
import pandas as pd
import re
import numpy as np
from other_function import drop_num, drop_num_2

base_path = r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2015 ' \
            r'г/ФОРМА 55/для программы'
papki = [x for x in os.listdir(base_path) if x.endswith(('.xls', '.xlsx'))]


