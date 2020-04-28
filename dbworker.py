import sqlite3
from datetime import datetime
conn = sqlite3.connect("base.db")
print('БД подключена...')
c = conn.cursor()

#проверяет есть ли пользователь с таким ID в БД
def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True

#добавляет нового пользователя с его данными
def register_new_user(UserID, UserLastName, UserFirstName, UserSex, UserCountry, UserCity, UserDomain, UserPhoto200):

    new_user_param = (UserID, 1, 0)
    print(new_user_param)
    c.execute("INSERT INTO users (user_id, user_reg, user_admin) VALUES (?,?,?)", new_user_param)
    conn.commit()

    new_user_info_param = (UserID, UserLastName, UserFirstName, UserSex, UserCountry, UserCity, UserDomain, UserPhoto200)
    print(new_user_info_param)
    c.execute("INSERT INTO users_info (user_id, user_lastname, user_firstname, user_sex, user_country, user_city, user_domain, user_photo_200) VALUES (?,?,?,?,?,?,?,?)", new_user_info_param)
    conn.commit()

#получает значение из столбца статуса администратора (1 - админ, 0 - пользователь)
def get_admin_status(user_id):
    c.execute("SELECT user_admin FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]

# def set_user_wish(user_id, user_wish):
#     c.execute("UPDATE user_info SET user_wish = %d WHERE user_id = %d" % (user_wish, user_id))
#     conn.commit()
