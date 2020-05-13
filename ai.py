#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import os
import random
import re
import time
import apiai
import psycopg2
from func import *
from keyboard import *
from parse import *
from parse_sgspu import *
import vk_api

logging.basicConfig(filename="vkbot.log", level=logging.INFO)
logging.info("Start AbituentBotVk! " + str(datetime.now()))

token = os.environ.get('TOKEN_ABITUR')
vk_session = vk_api.VkApi(token=token)

global Random


def random_chat_id():
    chat_id = 0
    chat_id += random.randint(0, 1000000000)
    return chat_id


ans = Constants


def ais(msg):
    request = apiai.ApiAI('5ccf3dbe9f594b97abe53c8332dc1e90').text_request()  # Токен API к DialogFlow
    request.lang = 'ru'  # Язык
    request.query = msg  # Посылаем сообщение в DialogFlow
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON
    return response


def main():
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            vk = vk_session.get_api()
            print(colorama.Fore.LIGHTGREEN_EX + '[x] Соединение установлено...')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text.lower()
                    if ais(msg) is None:
                        print(ais(msg))
                    else:
                        if not check_if_exists(event.user_id):
                            user_data = vk.users.get(user_ids=event.user_id,
                                                     fields="last_name, firstname, sex, country, city, domain, "
                                                            "photo_200")
                            get_profile_vk(user_data)
                        if msg in ('/start', 'начать', '📖 вернуться назад', 'назад к главной', 'вернуться назад к главной'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message=ans.start_info,
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                        elif msg in ('/my_ball', '📖 мои баллы'):
                            if get_status_ball(event.user_id):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="✅ Все ваши баллы указанны ниже: \n\n" + get_my_ball(event.user_id),
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="⚠ Вы не добавили баллы!",
                                    keyboard=keyboard_add_ball(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/add_ball', '📖 добавить баллы', 'показать предыдущие предметы'):
                            if get_status_ball(event.user_id):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="✅ Все ваши баллы указанны ниже: \n\n" + get_my_ball(event.user_id),
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_add_ball(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/add_ball_2', '📖 добавить баллы 2', 'показать следующие предметы'):
                            if get_user_ball_status(event.user_id) == 1:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Ваши баллы: ",
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_subject_2(),
                                    random_id=random_chat_id()
                                )
                        elif event.text in (
                                '🧮 Профильная математика', '🇷🇺 Русский язык', '🏘 Обществознание', '🧬 Биология',
                                '⚛ Физика',
                                '🏰 История', '💻 Информатика', '🧪 Химия', '📝 Литература', '🗺 География'):
                            if event.text == '🧮 Профильная математика':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🧮 Введите количество баллов по Профильной математике: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 1)
                            elif event.text == '🇷🇺 Русский язык':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🇷🇺 Введите количество баллов по Русскому языку: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 2)
                            elif event.text == '🏘 Обществознание':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🏘 Введите количество баллов по Обществознанию: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 3)
                            elif event.text == '🧬 Биология':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🧬 Введите количество баллов по Биологии: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 4)
                            elif event.text == '⚛ Физика':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="⚛ Введите количество баллов по Физике: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 5)
                            elif event.text == '🏰 История':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🏰 Введите количество баллов по Истории: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 6)
                            elif event.text == '💻 Информатика':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="💻 Введите количество баллов по Информатике: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 7)
                            elif event.text == '🧪 Химия':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🧪 Введите количество баллов по Химии: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 8)
                            elif event.text == '📝 Литература':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="📝 Введите количество баллов по Литературе: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 9)
                            elif event.text == '🗺 География':
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🗺 Введите количество баллов по Географии: ",
                                    keyboard=keyboard_insert_ball(),
                                    random_id=random_chat_id()
                                )
                                set_user_choose_subject(event.user_id, 10)
                        elif msg in ('/back_to_add_ball', '📖 назад к выбору предмета', 'отмена добавления балла'):
                            set_user_choose_subject(event.user_id, 0)
                            if get_user_ball_status(event.user_id) == 1:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Ваши баллы: ",
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                        elif (re.match(r"\d\d", event.text)) or (re.match(r"\d\d\d", event.text)):
                            set_user_ball(event.user_id, get_user_choose_subject(event.user_id), event.text)
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🔰Вы ввели: " + event.text + "\n✔Баллы по предмету обновлены!",
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                            set_user_choose_subject(event.user_id, 0)
                        elif msg in ('/remove_ball_to_choose_subject', '📖 удалить баллы по этому предмету'):
                            set_user_ball(event.user_id, get_user_choose_subject(event.user_id), 0)
                            if get_status_ball(event.user_id):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="✔Баллы у предмета удалены! \n\n" + get_my_ball(event.user_id),
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="🔰Выберите предмет, который хотите добавить!",
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="✔Баллы у предмета удалены!\nБольше баллов нет. Добавьте их!",
                                    keyboard=keyboard_subject_1(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/view_spec', '📒 направления и специальности', 'направления и специальности'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="📒Выберите: ",
                                keyboard=keyboard_spec(),
                                random_id=random_chat_id()
                            )
                        elif msg in ('/spec_bakalavr', '📒 бакалавриат', 'бакалавриат'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="⚠ Все специальности и направления\nбакалавриата и информация\n о них ниже: ",
                                keyboard=keyboard_spec(),
                                random_id=random_chat_id()
                            )
                            bakalavrList = view_abitur_bakalavr()
                            for i in range(len(bakalavrList)):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=bakalavrList[i],
                                    keyboard=keyboard_spec(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/spec_magist', '📒 магистратура', 'магистратура'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="⚠ Все специальности и направления\nмагистратуры и информация\n о них ниже: ",
                                keyboard=keyboard_spec(),
                                random_id=random_chat_id()
                            )
                            magistrList = view_abitur_magistr()
                            for i in range(len(magistrList)):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=magistrList[i],
                                    keyboard=keyboard_spec(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/view_news', '📰 новости с сайта самгупс', 'новости сайта'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message='❓Хочешь увидеть последнюю или последние 10 новостей?',
                                keyboard=keyboard_choose_news(),
                                random_id=random_chat_id()
                            )
                        elif msg in ('/view_all_news', '📰 показать 10 последних', 'показать 10 последних'):
                            newsList = view_all_news()
                            for i in range(len(newsList)):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message=newsList[i],
                                    keyboard=keyboard_choose_news(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/view_last_news', '📰 последняя', 'последняя'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message='' + view_last_news(),
                                keyboard=keyboard_choose_news(),
                                random_id=random_chat_id()
                            )
                        elif msg in ('/zvonok', '⏲ когда звонок?', '/когда звонок?'):
                            if (str(para(1) == None) or str(para(2) == None)):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Сейчас переменна! Отдыхай.',
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Сейчас: ' + str(para(1)) + '\n⌛Закончится через - ' + str(para(2)) + ' минут!',
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/week_lk', '📅 какая неделя?', '/weeks_lk'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message='' + weekFull(),
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                        elif msg in (
                                '/админ', 'админ', '/admin', 'администратор', 'admin', 'админ-панель'):
                            if get_admin_status(event.user_id) == 1:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Добро пожаловать в Админ-панель\nID Админа: ' + str(event.user_id),
                                    keyboard=keyboard_start_admin(),
                                    random_id=random_chat_id()
                                )
                            elif get_admin_status(event.user_id) == 0:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Вы не являетесь администратором!',
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                        elif msg in (
                                '/ob', '❗ сделать объявление', '❗ Сделать объявление', 'объявление', '/объявление'):
                            if get_admin_status(event.user_id) == 1:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Чтобы написать сообщения всем,\nоформите сообщение по шаблону (ниже):\n '
                                            '!объявление: текст-текст-текст ',
                                    keyboard=keyboard_start_admin(),
                                    random_id=random_chat_id()
                                )
                            elif get_admin_status(event.user_id) == 0:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Нет прав доступа!',
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                        elif msg in ('/view_ob', '📣 показать объявления', 'показать объявления'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message=get_last_ob(),
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                        elif re.match(r'!объявление', event.text):
                            ob_parse = re.split(r': ', event.text)
                            ob_str = ob_parse[1]
                            vk.messages.send(
                                user_id=event.user_id,
                                message='📣 Ваше объявление %s' % ob_str + '\nуспешно добавленно в очередь!',
                                keyboard=keyboard_start_admin(),
                                random_id=random_chat_id()
                            )
                            add_new_ob(ob_str)
                        elif event.text.lower() in (
                                '/my', '✅ моё расписание', 'мое расписание', 'моё расписание', '✅ мое расписание',
                                '/myrasp'):
                            if get_user_group(event.user_id) != 0:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Твоя группа: ' + get_user_group(event.user_id),
                                    keyboard=enable_keyboard_week(event.user_id),
                                    random_id=random_chat_id()
                                )
                            elif get_user_group(event.user_id) == 0:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Вы не добавили группу!\nЧтобы это сделать, введите группу\nДля этого '
                                            'введите фразу и вашу группу, пример ниже:\n\n Моя группа: ФМФИ-б18ПИо',
                                    keyboard=keyboard_start(),
                                    random_id=random_chat_id()
                                )
                        elif re.match(r'Моя группа', event.text):
                            mygroup_parse = re.split(r': ', event.text)
                            user_group = mygroup_parse[1]
                            set_user_group(event.user_id, user_group)
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Твоя группа - %s' % user_group + '\nуспешно обновленна в базе!',
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )
                        elif (re.match(r"\w\w\w\w-\w\d\d\w\w\w", event.text)) or (re.match(r"\w\w\w\w-\w\d\d\w\w", event.text)):
                            if get_user_group(event.user_id) != 0:
                                set_user_group(event.user_id, event.text)
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Ваш выбор: ' + get_user_group(event.user_id),
                                    keyboard=enable_keyboard_week(event.user_id),
                                    random_id=random_chat_id()
                                )
                        elif event.text.lower() in ('пн', 'вт', 'ср', 'чт', 'пт', 'сб'):
                            if get_user_group(event.user_id) != 0:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Выбранный день недели: ' + event.text + '\nВыбранная группа: ' + get_user_group(
                                        event.user_id),
                                    keyboard=enable_keyboard_week(event.user_id),
                                    random_id=random_chat_id()
                                )
                                if (event.text == 'ПН' or event.text == 'пн'):
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=get_mon(get_user_group(event.user_id)),
                                        keyboard=enable_keyboard_week(event.user_id),
                                        random_id=random_chat_id()
                                    )
                                elif (event.text == 'ВТ' or event.text == 'вт'):
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=get_tue(get_user_group(event.user_id)),
                                        keyboard=enable_keyboard_week(event.user_id),
                                        random_id=random_chat_id()
                                    )
                                elif (event.text == 'СР' or event.text == 'ср'):
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=get_mon(get_user_group(event.user_id)),
                                        keyboard=enable_keyboard_week(event.user_id),
                                        random_id=random_chat_id()
                                    )
                                elif (event.text == 'ЧТ' or event.text == 'чт'):
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=get_thu(get_user_group(event.user_id)),
                                        keyboard=enable_keyboard_week(event.user_id),
                                        random_id=random_chat_id()
                                    )
                                elif (event.text == 'ПТ' or event.text == 'пт'):
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=get_fri(get_user_group(event.user_id)),
                                        keyboard=enable_keyboard_week(event.user_id),
                                        random_id=random_chat_id()
                                    )
                                elif (event.text == 'СБ' or event.text == 'сб'):
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=get_sab(get_user_group(event.user_id)),
                                        keyboard=enable_keyboard_week(event.user_id),
                                        random_id=random_chat_id()
                                    )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message=ais(msg),
                                keyboard=keyboard_start(),
                                random_id=random_chat_id()
                            )

        except Exception as e:
            logging.error(str(datetime.now()) + " " + str(e))
            time.sleep(10)


if __name__ == '__main__':
    main()
