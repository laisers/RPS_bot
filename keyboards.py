from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

""" Клавиатура в главном меню """


def but_menu():
    mainkeyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    mainkeyboard.row('🎲 Играть', '📙 Личный кабинет')
    mainkeyboard.row('🔰 Документация')
    return mainkeyboard


""" Клавиатура с кнопкой вернуться назад """


def but_back():
    keyboardback = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboardback.row('Вернуться в главное меню')
    return keyboardback


""" Админская клавиатура """


def but_admin():
    keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_admin.row('Статистика бота')
    keyboard_admin.row('Управление балансом', 'Вернуться в главное меню')
    return keyboard_admin


""" Игровая клавиатура """
keyboard_game = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_game.row('✊ Камень', '✌ Ножницы', '🤚 Бумага')
keyboard_game.row('Вернуться в главное меню')

""" Inline клавиатуры """
inline_profile = InlineKeyboardMarkup()
inline_profile.add(InlineKeyboardButton('💸 Пополнить баланс', callback_data='paybal_inline'))
# inline_profile.add(InlineKeyboardButton('💸 Пополнить баланс', callback_data='paybal_inline'),
#                    InlineKeyboardButton('⚙️ Настройки', callback_data='settings_inline'))


""" Прочие клавиатуры """
settings_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

settings_keyboard.row('🎉 Включить/выключить рассылки')
settings_keyboard.row('🗑 Включить/выключить новый дизайн (in dev)')
settings_keyboard.row('Вернуться в главное меню')
