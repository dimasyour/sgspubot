import sqlite3
import Constants
import colorama
from datetime import datetime

slova = Constants

conn = sqlite3.connect("src/base.db")
print(colorama.Fore.LIGHTGREEN_EX + '[x] БД подключена...')
c = conn.cursor()


# проверяет есть ли пользователь с таким ID в БД
def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True


# добавляет нового пользователя с его данными
def register_new_user(UserID, UserLastName, UserFirstName, UserSex, UserCountry, UserCity, UserDomain, UserPhoto200):
    new_user_param = (UserID, 1, 0, 0, 0)
    c.execute("INSERT INTO users (user_id, user_reg, user_admin, user_ball, user_group) VALUES (?,?,?,?)",
              new_user_param)
    conn.commit()

    new_user_info_param = (
        UserID, UserLastName, UserFirstName, UserSex, UserCountry, UserCity, UserDomain, UserPhoto200)
    c.execute(
        "INSERT INTO users_info (user_id, user_lastname, user_firstname, user_sex, user_country, user_city, user_domain, user_photo_200) VALUES (?,?,?,?,?,?,?,?)",
        new_user_info_param)
    conn.commit()

    new_user_ball_param = (UserID, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    c.execute(
        "INSERT INTO user_ball (user_id, user_choose, math_p, russ, obsh, biol, phys, isto, info, himi, lite, geog, lang_e) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        new_user_ball_param)
    conn.commit()


# получает значение из столбца статуса администратора (1 - админ, 0 - пользователь)
def get_admin_status(user_id):
    c.execute("SELECT user_admin FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


# получает значение из столбца статуса баллов (1 - добавил баллы, 0 - не добавил)
def get_user_ball_status(user_id):
    c.execute("SELECT user_ball FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


# записывает, какой предмет абитуриент, хочет выбрать, чтобы добавить баллы к нему (0 - выйти из добавления)
def set_user_choose_subject(user_id, subject_id):
    c.execute("UPDATE user_ball SET user_choose = %d WHERE user_id = %d" % (subject_id, user_id))
    conn.commit()


# изменяет баллы по выбранному предмету
def set_user_ball(user_id, subject, ball):
    if subject == 1:
        c.execute("UPDATE user_ball SET math_p = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 2:
        c.execute("UPDATE user_ball SET russ = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 3:
        c.execute("UPDATE user_ball SET obsh = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 4:
        c.execute("UPDATE user_ball SET biol = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 5:
        c.execute("UPDATE user_ball SET phys = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 6:
        c.execute("UPDATE user_ball SET isto = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 7:
        c.execute("UPDATE user_ball SET info = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 8:
        c.execute("UPDATE user_ball SET himi = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 9:
        c.execute("UPDATE user_ball SET lite = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 10:
        c.execute("UPDATE user_ball SET geog = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()
    elif subject == 11:
        c.execute("UPDATE user_ball SET lang_e = %s WHERE user_id = %d" % (ball, user_id))
        conn.commit()


# узнает к какому предмету хочет добавить студент баллы
def get_user_choose_subject(user_id):
    c.execute("SELECT user_choose FROM user_ball WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


# показать баллы абитуриента
def get_my_ball(user_id):
    c.execute(
        "SELECT math_p, russ, obsh, biol, phys, isto, info, himi, lite, geog, lang_e FROM user_ball WHERE user_id = %d" % user_id)
    result = c.fetchone()
    i = 0
    myballs = []
    for i in range(11):
        if result[i] != 0:
            myballs.append(slova.subject[i] + ": " + str(result[i]))
            myballsString = '\n'.join(myballs)
    return myballsString


# проверяет есть ли хотя бы один предмет с добавленными баллами
def get_status_ball(user_id):
    c.execute(
        "SELECT math_p, russ, obsh, biol, phys, isto, info, himi, lite, geog, lang_e FROM user_ball WHERE user_id = %d" % user_id)
    result = c.fetchone()
    res = 0
    for i in range(0, 11):
        if result[i] != 0:
            res = res + 1
    if res > 0:
        return True
    else:
        return False


def get_user_group(user_id):
    c.execute("SELECT user_group FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


def set_user_group(user_id, user_group):
    c.execute("UPDATE users SET user_group=? WHERE user_id=?", (user_group, user_id))
    conn.commit()


def add_new_ob(text):
    date_ob = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M")
    c.execute("INSERT INTO ob_table(date_ob, text_ob) VALUES ('%s','%s')" % (date_ob, text))
    conn.commit()


def get_last_ob():
    c.execute("SELECT text_ob,date_ob FROM ob_table WHERE id=(SELECT MAX(id) FROM ob_table)")
    rows = c.fetchall()
    for row in rows:
        return '❗Последнее объявление: ' + row[0] + '\n\nДобавленно: ' + row[1]
