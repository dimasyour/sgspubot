#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import random
import re
import vk_api, random
import time
import logging
import Constants
from vk_api.longpoll import *
from vk_api.utils import get_random_id
from datetime import datetime

from keyboard import *
from dbworker import *

logging.basicConfig(filename="vkbot.log", level=logging.INFO)
logging.info("Start AbituentBotVk! " + str(datetime.now()))

token = os.environ.get('TOKEN_ABITUR')
vk_session = vk_api.VkApi(token=token)


global Random

def random_id():
    Random = 0
    Random += random.randint(0, 1000000000);
    return Random

ans = Constants

def main():
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            vk = vk_session.get_api()
            print('Соединение установлено...')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text.lower()
                    if not check_if_exists(event.user_id):
                        # получаем данные о пользователе (vk.com/dev/users.get)
                        user_data = vk.users.get(user_ids = event.user_id, fields="last_name, firstname, sex, country, city, domain, photo_200")
                        UserID = user_data[0]["id"]
                        UserLastName = user_data[0]["last_name"]
                        UserFirstName = user_data[0]["first_name"]
                        UserSex = user_data[0]["sex"]
                        UserCountry = user_data[0]["country"]['title']
                        UserCity = user_data[0]["city"]['title']
                        UserDomain = user_data[0]["domain"]
                        UserPhoto200 = user_data[0]["photo_200"]
                        register_new_user(UserID, UserLastName, UserFirstName, UserSex, UserCountry, UserCity, UserDomain, UserPhoto200)

                    if msg in ('/start', 'начать', '📖 вернуться назад'):
                        vk.messages.send(
                            user_id=event.user_id,
                            message="Бот работает!",
                            keyboard=keyboard_start(),
                            random_id=random_id()
                        )
                    elif msg in ('/my_ball', '📖 мои баллы'):
                        if (get_user_ball_status(event.user_id) == 1):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="Ваши баллы: ",
                                keyboard=keyboard_start(),
                                random_id=random_id()
                            )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="⚠ Вы не добавили баллы!",
                                keyboard=keyboard_add_ball(),
                                random_id=random_id()
                            )
                    elif msg in ('/add_ball', '📖 добавить баллы', 'показать предыдущие предметы'):
                        if (get_user_ball_status(event.user_id) == 1):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="Ваши баллы: ",
                                keyboard=keyboard_start(),
                                random_id=random_id()
                            )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🔰Выберите предмет, который хотите добавить!",
                                keyboard=keyboard_subject_1(),
                                random_id=random_id()
                            )
                    elif msg in ('/add_ball_2', '📖 добавить баллы 2', 'показать следующие предметы'):
                        if (get_user_ball_status(event.user_id) == 1):
                            vk.messages.send(
                                user_id=event.user_id,
                                message="Ваши баллы: ",
                                keyboard=keyboard_start(),
                                random_id=random_id()
                            )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message="🔰Выберите предмет, который хотите добавить!",
                                keyboard=keyboard_subject_2(),
                                random_id=random_id()
                            )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            message="Неизвестная команда",
                            keyboard=keyboard_start(),
                            random_id=random_id()
                        )
        except Exception as e:
            logging.error(str(datetime.now()) + " " +str(e))
            time.sleep(10)

if __name__ == '__main__':
    main()