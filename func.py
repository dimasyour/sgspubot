import pandas as pd
import vk_api
from openpyxl import load_workbook
from vk_api.longpoll import *
from dbworker import *

print(colorama.Fore.LIGHTBLUE_EX + 'Парсинг новостей - успешно!')


def parse_table_spec():
    url = "https://www.samgups.ru/education/abiturientam/pk-2020-vo/samara/spetsialnosti_i_napravleniya_podgotovki/index.php"
    table = pd.read_html(url)[0]
    table.to_excel("src/ochnik.xlsx")
    table = pd.read_html(url)[1]
    table.to_excel("src/zaochnik.xlsx")


def view_spec(file):
    wb1 = load_workbook(file)
    sheet_ranges = wb1['Sheet1']
    column_b = sheet_ranges['B']
    column_c = sheet_ranges['C']
    column_d = sheet_ranges['D']

    specList = []
    for i in range(5, len(column_c)):
        if column_b[i].value != 'БАКАЛАВРИАТ (срок обучения - 4 года)':
            f = ' ' + column_d[i].value.replace(',', '\n')
            specList.append('❗' + column_b[i].value + '\n✅ ' + column_c[i].value + ': \n' + f + '\n\n')
        elif column_b[i].value != '':
            break
    specString = '\n'.join(specList)
    return specString


# парситься JSON и занесение этих данных в БД (регистрация)
def get_profile_vk(user_data):
    UserID = user_data[0]["id"]
    UserLastName = user_data[0]["last_name"]
    UserFirstName = user_data[0]["first_name"]
    UserSex = user_data[0]["sex"]
    UserCountry = user_data[0]["country"]['title']
    UserCity = user_data[0]["city"]['title']
    UserDomain = user_data[0]["domain"]
    UserPhoto200 = user_data[0]["photo_200"]
    register_new_user(UserID, UserLastName, UserFirstName, UserSex, UserCountry, UserCity, UserDomain, UserPhoto200)
