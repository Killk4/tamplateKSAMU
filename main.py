import re
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
                10 : 'надпись',
                11 : 'автоподстановочное поле', # Найти что подставляет
                12 : 'таблица',
                13 : 'результаты исследований', # скорее всего из БД в рамках текущей истории болезни
                14 : 'переключатели (радио)',
                15 : 'DICOM',
                16 : 'галочки (чек боксы)',
                17 : 'список с галочками (чек боксами)'}

elemet_parameters = ['list_of_values', 'obiazatpole', 'user_tree_element_name']

with open('530н Первичный осмотр.xml', 'r', encoding='utf-8') as file:
    
    i = 1
    lin = 0
    elist = 0
    count = 0
    type_nn = 0

    for line in file:
        res = re.match(r'.*<Elem.* P', line)
        if res is not None:
            print(f'{i}: {res.group(0)}')
            count = count + 1
            type_nn = re.search(r'TYP="[0-9]*"', line).group(0)[5:-1]
        if int(type_nn) != 0:
            res = re.search(r'listofvalues=".*', line)
            if res is not None:

                list_is_none = re.search(r'listofvalues=""', line)
                if list_is_none is None:
                    lin = 0
                else:
                    lin = 1
                    type_nn = 0

                end_list = re.search(r'".*height', line)
                if end_list is not None:
                    elist = 1
                    type_nn = 0
                else:
                    elist = 0
                
            if lin == 0 and elist == 0:
                print(line)
            

        i = i+1
        sleep(.005)

print(f'Найдено совпадений {count}')

