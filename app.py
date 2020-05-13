#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import os
import random
import re
import time
from flask import Flask
import apiai

from func import *
from keyboard import *
from parse import *

app = Flask(__name__)

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

@app.route('/ai', methods=['POST', 'GET'])
def ais(msg):
    request = apiai.ApiAI('5ccf3dbe9f594b97abe53c8332dc1e90').text_request()  # Токен API к DialogFlow
    request.lang = 'ru'  # Язык
    request.query = msg  # Посылаем сообщение в DialogFlow
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON
    return response

@app.route('/', methods=['POST', 'GET'])
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
                                                     fields="last_name, firstname, sex, country, city, domain, photo_200")
                            get_profile_vk(user_data)
                        if msg in ('/start', 'начать', '📖 вернуться назад', 'назад к главной'):
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
                                    message="✅ Все ваши баллы указанны ниже: \n\n"+get_my_ball(event.user_id),
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
                                    message="✅ Все ваши баллы указанны ниже: \n\n"+get_my_ball(event.user_id),
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
                                    message="✔Баллы у предмета удалены! \n\n"+get_my_ball(event.user_id),
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
                                message="📒Выберите форму обучения: ",
                                keyboard=keyboard_spec(),
                                random_id=random_chat_id()
                            )
                        elif msg in ('/spec_och', '📒 очная', 'очная'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="⚠ Все специальности и направления\nочной формы обучения\n ниже: ",
                                keyboard=keyboard_spec(),
                                random_id=random_chat_id()
                            )
                            vk.messages.send(
                                user_id=event.user_id,
                                message=view_spec('src/ochnik.xlsx'),
                                keyboard=keyboard_spec(),
                                random_id=random_chat_id()
                            )
                        elif msg in ('/spec_zaoch', '📒 заочная', 'заочная'):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="⚠ Все специальности и направления\nзаочной формы обучения\n ниже: ",
                                keyboard=keyboard_spec(),
                                random_id=random_chat_id()
                            )
                            vk.messages.send(
                                user_id=event.user_id,
                                message=view_spec('src/zaochnik.xlsx'),
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


port = int(os.environ.get('PORT', 8080))
if __name__ == "__main__":
    app.run(debug=True, port=port)
