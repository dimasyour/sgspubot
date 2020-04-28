from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def keyboard_start(geo_button=False):
    keyboard = VkKeyboard(False)
    keyboard.add_button('📖 Мои баллы', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Список', VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()
