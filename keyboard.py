from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from dbworker import *


def keyboard_start():
    keyboard = VkKeyboard(False)
    keyboard.add_button('📖 Мои баллы', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('📒 Направления и специальности', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('⏲ Когда звонок?', VkKeyboardColor.POSITIVE)
    keyboard.add_button('📅 Какая неделя?', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('📣 Показать объявления', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('✅ Моё расписание', VkKeyboardColor.POSITIVE)
    # keyboard.add_button('📰 Новости с сайта СамГУПС', VkKeyboardColor.POSITIVE)
    # keyboard.add_line()
    keyboard.add_openlink_button('Группа ВК', 'http://vk.com/pgsga')

    return keyboard.get_keyboard()


def keyboard_start_admin():
    keyboard = VkKeyboard(False)
    keyboard.add_button('📖 Мои баллы', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('📒 Направления и специальности', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('⏲ Когда звонок?', VkKeyboardColor.POSITIVE)
    keyboard.add_button('📅 Какая неделя?', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('✅ Моё расписание', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('📣 Показать объявления', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('❗ Сделать объявление', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    # keyboard.add_button('📰 Новости с сайта СамГУПС', VkKeyboardColor.POSITIVE)
    # keyboard.add_line()
    keyboard.add_openlink_button('Группа ВК', 'http://vk.com/pgsga')

    return keyboard.get_keyboard()


def keyboard_add_ball():
    keyboard = VkKeyboard(False)
    keyboard.add_button('📖 Добавить баллы', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('📖 Вернуться назад', VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()


def keyboard_subject_1():
    keyboard = VkKeyboard(False)
    keyboard.add_button('Показать следующие предметы', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('🧮 Профильная математика', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🇷🇺 Русский язык', VkKeyboardColor.PRIMARY)
    keyboard.add_button('🏘 Обществознание', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🧬 Биология', VkKeyboardColor.PRIMARY)
    keyboard.add_button('⚛ Физика', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📖 Вернуться назад', VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def keyboard_subject_2():
    keyboard = VkKeyboard(False)
    keyboard.add_button('Показать предыдущие предметы', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('🏰 История', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('💻 Информатика', VkKeyboardColor.PRIMARY)
    keyboard.add_button('🧪 Химия', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📝 Литература', VkKeyboardColor.PRIMARY)
    keyboard.add_button('🗺 География', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📖 Вернуться назад', VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def keyboard_insert_ball():
    keyboard = VkKeyboard(False)
    keyboard.add_button('📖 Удалить баллы по этому предмету', VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('📖 Назад к выбору предмета', VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def keyboard_spec():
    keyboard = VkKeyboard(False)
    keyboard.add_button('📒 Бакалавриат', VkKeyboardColor.PRIMARY)
    keyboard.add_button('📒 Магистратура', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Назад к главной', VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()


def keyboard_choose_news():
    keyboard = VkKeyboard(False)
    keyboard.add_button('📰 Последняя', VkKeyboardColor.PRIMARY)
    keyboard.add_button('📰 Показать 10 последних', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Назад к главной', VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()


def enable_keyboard_week(user_id):
    keyboard = VkKeyboard(False)
    keyboard.add_button(get_user_group(user_id), VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('ПН', VkKeyboardColor.POSITIVE)
    keyboard.add_button('ВТ', VkKeyboardColor.POSITIVE)
    keyboard.add_button('СР', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('ЧТ', VkKeyboardColor.POSITIVE)
    keyboard.add_button('ПТ', VkKeyboardColor.POSITIVE)
    keyboard.add_button('СБ', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Вернуться назад к главной', VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()
