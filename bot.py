#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import re
import time
import random
import vk_api
from vk_api.longpoll import *
import apiai, json
from dbworker import *
from keyboard import *
from func import *

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


def main():
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            vk = vk_session.get_api()
            print('Соединение установлено...')
            parse_html_html()
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text.lower()
                    if not check_if_exists(event.user_id):
                        # получаем данные о пользователе (vk.com/dev/users.get)
                        user_data = vk.users.get(user_ids=event.user_id,
                                                 fields="last_name, firstname, sex, country, city, domain, photo_200")
                        UserID = user_data[0]["id"]
                        UserLastName = user_data[0]["last_name"]
                        UserFirstName = user_data[0]["first_name"]
                        UserSex = user_data[0]["sex"]
                        UserCountry = user_data[0]["country"]['title']
                        UserCity = user_data[0]["city"]['title']
                        UserDomain = user_data[0]["domain"]
                        UserPhoto200 = user_data[0]["photo_200"]
                        register_new_user(UserID, UserLastName, UserFirstName, UserSex, UserCountry, UserCity,
                                          UserDomain, UserPhoto200)
                        request = apiai.ApiAI('b2abbedff7cb47b89ac725d08f0436cb  ').text_request() # Токен API к DialogFlow
                        request.lang = 'ru' # Язык
                        request.query = event.text # Посылаем сообщение в DialogFlow                    
                        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
                        response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON
                        print(response)
                        # try:
                        if re.match(r'vk', response) or re.match(r'if ', response):
                                exec(response)
                        else:
                                vk.messages.send(
                                    user_id = event.user_id,
                                    random_id = event.random_id,
                                    message = 'не найдено'
                                )
        except Exception as e:
            logging.error(str(datetime.now()) + " " + str(e))
            time.sleep(10)


if __name__ == '__main__':
    main()
