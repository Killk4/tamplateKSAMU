import re
import os
from time import sleep

# типы элементов
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

# функция логгирования
def log(text:str, filename:str)-> bool:
    with open(f'./after/{filename}.txt', 'a', encoding='utf8') as file:
        file.write(text)
        print(text)
            

# перебираем все файлы из папки before
for filename in os.listdir('./before/'):
    if (os.path.isfile(f'./before/{filename}') is False) or (filename == '.gitkeep'): # если не файл или .getkeep, то скипаем
        continue

    # открываем файл из папки before
    with open(f'./before/{filename}', 'r', encoding='utf-8') as file:
        
        i = 1           # номер строки в файле
        lin = 1         # бул на проверку пустых значений в поле
        elist = 1       # бул на проверку конца списка
        val_exist = 1   # бул на проверку элемента
        count = 0       # счётчик найденных элементов
        type_nn = 0     # номер типа элемента (0 - папка)

        # переборка файла
        for line in file:

            # поиск начала элемента "<Element_1..."
            res = re.match(r'.*<Elem.* P', line)
            if res is not None:
                count = count + 1
                type_nn = re.search(r'TYP="[0-9]*"', line).group(0)[5:-1]   # присваиваем тип элемента
            if int(type_nn) != 0:   # если не папка

                tree_fiel_name = re.search(r'user_tree_element_name=".*".*prog', line)  # имя элемента в дереве шаблонизатора
                
                full_field_name = re.search(r'nadpis_text=".*".*nadpis', line)  # имя в label элемента

                # обрезаем распарсенные данные до значений
                if full_field_name is not None:
                    field_name = re.search(r'".*"', full_field_name.group(0))
                    t_field_name = re.search(r'".*"', tree_fiel_name.group(0))
                    # пишем в файл название элемента v
                    log(f'\nНазвание поля -> "{field_name.group(0)[1:-21]}" ({elemet_types[int(type_nn)]}) (переменная: {t_field_name.group(0)[1:-1]})\n', filename)

                # ищем список значений
                res = re.search(r'listofvalues=".*', line)
                if res is not None:
                    line = re.search(r's=".*', res.group(0)).group(0)[3:]   # получаем первое значение
                    val_exist = 0

                list_is_none = re.search(r'listofvalues=""', line)  # если пусто, то скипаем
                if list_is_none is None:
                    lin = 0
                else:
                    lin = 1
                    type_nn = 0

                end_list = re.search(r'".*height', line) # проверка конца списка значений
                if end_list is not None:
                    elist = 1
                    type_nn = 0
                    val_exist = 1
                else:
                    elist = 0
                    
                # если все звёзды сошлись, то пишем строку в файл
                if lin == 0 and elist == 0 and val_exist == 0:
                    log(line, filename)

            i = i+1
            sleep(.005)

        print(f'Найдено совпадений {count}')

