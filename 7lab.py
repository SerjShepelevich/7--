#1) Вручную создать текстовый файл с данными (например, марка авто, модель авто, расход топлива, стоимость).
#
#2) Создать doc шаблон, где будут использованы данные параметры.
from sqlalchemy.dialects.postgresql import json

st1 = ('BMW', 'E81-E82-E87-E88', 'рестайлинг', 'Кабриолет', '143 л.с.', 12000)
st2 = ('BMW', 'E81/E82/E87/E88', 'рестайлинг', 'Купе', '143 л.с.', 12500)
st3 = ('BMW', 'E81/E82/E87/E88', 'рестайлинг', 'Хетчбэк 3-дв.',	'115 л.с.', 15000)

with open('data','w') as f:
    f.write(str(st1)+'\n')
    f.write(str(st2)+'\n')
    f.write(str(st3)+'\n')

with open('data','r') as f1:
    for line in f1:
        print(line)


#3) Автоматически сгенерировать отчет о машине в формате doc (как в видео 7.2).

import datetime
from docxtpl import DocxTemplate, InlineImage

def generate_temp(doc_temp,data_file):
    list_data = create_data_array(data_file)
    number = 0
    for line in list_data:
        create_file_report(doc_temp,line,number)
        number += 1

def create_data_array(data_file):
    import re
    with open(data_file,'r') as f:
        new_list=[]
        for line in f:
            line = (re.sub(r'[\'()\n]','',line)).split(',')
            new_dict = {'marka':line[0],
                        'generation':line[1],
                        'generation_type':line[2],
                        'seria':line[3],
                        'power':line[4],
                        'cost':line[5]}
            new_list.append(new_dict)
    return new_list

def create_file_report(doc_temp,line,number):
    template = DocxTemplate(doc_temp)
    template.render(line)
    template.save(line['marka']+str(number) + '_'+ str(datetime.datetime.now().date()) + '_report.docx')

generate_temp('report.docx','data')

#4) Создать csv файл с данными о машине.

def create_list_csv(data_file):
    list_of_data = create_data_array(data_file)
    data_to_csv = []
    keys = list_of_data[0].keys()
    data_to_csv.append(list(keys))
    for line in list_of_data:
        string = []
        for key in keys:
            string.append(line[key])
        data_to_csv.append(string)
    return data_to_csv

import csv

with open('example.csv','w', encoding='cp1251') as f:
    writer = csv.writer(f)
    writer.writerows(create_list_csv('data'))

#5) Создать json файл с данными о машине.

import json

dict_json = json.dumps(create_data_array('data'))

with open('example.json','w',encoding='cp1251') as f:
    json.dump(dict_json,f)

with open('example.json','r') as f1:
    data = json.load(f1)
print(data)
