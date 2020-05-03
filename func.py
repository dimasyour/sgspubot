import pandas as pd
import re
from openpyxl import load_workbook

def parse_html_html():
    url = "https://www.samgups.ru/education/abiturientam/pk-2020-vo/samara/spetsialnosti_i_napravleniya_podgotovki/index.php"
    table = pd.read_html(url)[0]
    table.to_excel("ochnik.xlsx")
    table = pd.read_html(url)[1]
    table.to_excel("zaochnik.xlsx")
    print('Таблицы специальностей и направлений успешно обновлены!')

def view_spec(forma):
	if (forma = 'очная'):
    	wb1 = load_workbook('ochnik.xlsx')
    elif (forma = 'заочная'):
    	wb1 = load_workbook('zaochnik.xlsx')
    else:
    	print('Нет такой формы')
    sheet_ranges = wb1['Sheet1']

    column_b = sheet_ranges['B']
    column_c = sheet_ranges['C']
    column_d = sheet_ranges['D']

    specList = []
    for i in range(5, len(column_c)):
        if  column_b[i].value != 'БАКАЛАВРИАТ (срок обучения - 4 года)':
        	# str1 = 'математика (27), физика (36), русский язык (36)'
            f = ' '+column_d[i].value.replace(',','\n')
            specList.append('❗'+column_b[i].value+'\n✅ '+column_c[i].value+': \n'+f+'\n\n')
        elif column_b[i].value != '':
            break
    specString = '\n'.join(specList)
    return specString

