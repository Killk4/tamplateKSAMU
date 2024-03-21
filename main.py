import re
import os
from time import sleep

#list_of_values="1
# 2
# 3
# 4"

#obiazatpole="0 or 1"

#user_tree_element_name="жалобы"

elemet_types = {0 : 'папка (группа)',
                1 : 'список из БД',
                2 : 'форматируемый текст (большое поле)',
                3 : 'целое число',
                4 : 'реквизиты из БД', #table_name из какой базы тянуть данные
                5 : 'текст',
                6 : 'дата и время',
                7 : 'список',
                8 : 'дробное число',
                9 : 'рисунок',
                10 : 'надпись (label)',
                11 : 'автоподстановочное поле', # Найти что подставляет
                12 : 'таблица',
                13 : 'результаты исследований', # скорее всего из БД в рамках текущей истории болезни
                14 : 'переключатели (радио)',
                15 : 'DICOM',
                16 : 'галочки (чек боксы)',
                17 : 'список с галочками (чек боксами)'}

elemet_parameters = ['list_of_values', 'obiazatpole', 'user_tree_element_name']

def log(text:str, filename:str)-> bool:
    with open(f'./after/{filename}.txt', 'a', encoding='utf8') as file:
        file.write(text)
        print(text)
            

for filename in os.listdir('./before/'):
    if (os.path.isfile(f'./before/{filename}') is False) or (filename == '.gitkeep'):
        continue

    with open(f'./before/{filename}', 'r', encoding='utf-8') as file:
        
        i = 1
        lin = 1
        elist = 1
        val_exist = 1
        count = 0
        type_nn = 0

        for line in file:

            res = re.match(r'.*<Elem.* P', line)
            if res is not None:
                count = count + 1
                type_nn = re.search(r'TYP="[0-9]*"', line).group(0)[5:-1]
            if int(type_nn) != 0:

                # is_required = re.search('obiazatpole')

                tree_fiel_name = re.search(r'user_tree_element_name=".*".*prog', line)
                
                full_field_name = re.search(r'nadpis_text=".*".*nadpis', line)
                if full_field_name is not None:
                    field_name = re.search(r'".*"', full_field_name.group(0))
                    t_field_name = re.search(r'".*"', tree_fiel_name.group(0))
                    log(f'\nНазвание поля -> "{field_name.group(0)[1:-21]}" ({elemet_types[int(type_nn)]}) (переменная: {t_field_name.group(0)[1:-1]})\n', filename)

                res = re.search(r'listofvalues=".*', line)
                if res is not None:
                    line = re.search(r's=".*', res.group(0)).group(0)[3:]
                    val_exist = 0

                list_is_none = re.search(r'listofvalues=""', line)
                if list_is_none is None:
                    lin = 0
                else:
                    lin = 1
                    type_nn = 0

                end_list = re.search(r'".*height', line) # тут нихуя не работает почему-то блять
                if end_list is not None:
                    elist = 1
                    type_nn = 0
                    val_exist = 1
                else:
                    elist = 0
                    
                if lin == 0 and elist == 0 and val_exist == 0:
                    log(line, filename)

            i = i+1
            sleep(.005)

        print(f'Найдено совпадений {count}')

