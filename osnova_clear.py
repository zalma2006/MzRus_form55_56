##
import os
import re
import warnings

warnings.filterwarnings('ignore')
DEBUG = True
from other_function import clear_df

forma = 55
if forma == 55:
    base_path = [r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2015 '
                 r'г/ФОРМА 55/для программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2016 '
                 r'г/ФОРМА 55/для программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2017 '
                 r'г/ФОРМА 55/для программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                 r'(2015-2020гг)/2018 г/ФОРМА 55/для программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                 r'(2015-2020гг)/2019 г/ФОРМА 55/для программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                 r'(2015-2020гг)/2020 г/ФОРМА 55/для программы']
if forma == 56:
    base_path = [r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2015'
                 r' г/ФОРМА 56/для_программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2016 '
                 r'г/ФОРМА 56/для_программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)/2017 '
                 r'г/ФОРМА 56/для_программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                 r'(2015-2020гг)/2018 г/ФОРМА 56/для_программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                 r'(2015-2020гг)/2019 г/ФОРМА 56/для_программы',
                 r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 '
                 r'(2015-2020гг)/2020 г/ФОРМА 56/для_программы']
print(base_path)
##
problems = {}
for x in base_path:
    c = ''.join(re.findall(r'\d+', x.split(r'/')[-3]))
    problems[c] = clear_df(base_path=x, forma=forma, problems=problems)
if forma == 55:
    os.chdir(r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)')
    with open('problems_form55.txt', 'w') as f:
        for key, val in problems.items():
            f.write(f'{key}: {val}\n')
if forma == 56:
    os.chdir(r'/media/maks/ntfs/Ирина/диссер статистика/Ф.55,56 (2015-2020гг)/Ф.55,56 (2015-2020гг)')
    with open('problems_form56.txt', 'w') as f:
        for key, val in problems.items():
            f.write(f'{key}: {val}\n')
##
print(problems.keys())
##
