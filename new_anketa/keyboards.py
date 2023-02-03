from aiogram import types

start_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_menu.add(*("➕", '❓'))

inline_send_data = types.InlineKeyboardMarkup()
b1 = types.InlineKeyboardButton(text="Да, отправить данные", callback_data="send_data")
b3 = types.InlineKeyboardButton(text="Отмена, назад в меню", callback_data="back_to_menu")
inline_send_data.add(b1)
inline_send_data.add(b3)

inline_send_data1 = types.InlineKeyboardMarkup()
b11 = types.InlineKeyboardButton(text="Ответить✅", callback_data="send_data1")
b22 = types.InlineKeyboardButton(text="Удалить❌", callback_data="edit_data1")
b33 = types.InlineKeyboardButton(text="Забанить🐷", callback_data="ban")
inline_send_data1.add(*(b11, b22))
inline_send_data1.add(b33)