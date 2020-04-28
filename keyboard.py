from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def keyboard_start(geo_button=False):
    keyboard = VkKeyboard(False)
    keyboard.add_button('регистрация', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('привет', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('ссылка', VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()
