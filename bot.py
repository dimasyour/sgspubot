#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import random
import re
import vk_api, random
import Constants
from vk_api.longpoll import *
from vk_api.utils import get_random_id
from keyboard import *
from dbworker import *

ans = Constants

token = os.environ.get('TOKEN_ABITUR')

vk_session = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()
print('Соединение установлено...')

dictStart = '''
Вот что я умею:
'''
global Random

def random_id():
    Random = 0
    Random += random.randint(0, 1000000000);
    return Random

while True:
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

            if msg == "привет":
                vk.messages.send(
                    user_id=event.user_id,
                    message="Привет!",
                    keyboard=keyboard_start(),
                    random_id=random_id()
                )
            elif msg == "ссылка":
                vk.messages.send(
                    user_id=event.user_id,
                    message="https://www.youtube.com/channel/UCCCcDxRXwTE-rtpcyMzxjAA?view_as=subscriber",
                    keyboard=keyboard_start(),
                    random_id=random_id()
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Неизвестная команда",
                    keyboard=keyboard_start(),
                    random_id=random_id()
                )