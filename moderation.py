import time
import telebot
from telebot import types
from configs.config_mate import TOKEN_Moder


bot = telebot.TeleBot(token=TOKEN_Moder)
admin_ids = []
user_admin = dict()


@bot.message_handler(commands=["start", "ask"])
def welcome(message):
    if message.chat.id in admin_ids:
        bot.send_message(message.chat.id, "Ждите сообщение от юзера!")
    else:
        if message.chat.id in user_admin:
            bot.send_message(message.chat.id, "Вы уже общаетесь с модератором!")
        else:
            flag = True
            for i in admin_ids:
                if i not in user_admin:
                    user_admin[message.chat.id] = i
                    user_admin[i] = message.chat.id
                    flag = False
                    break
            if flag:
                bot.send_message(message.chat.id, "Извините, но сейчас все пользователи заняты!\nПопробуйте позже.\n/ask")
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Завершить диалог")
                markup.add(btn1)
                bot.send_message(user_admin[message.chat.id], "К вам обратились за поддержкой", reply_markup=markup)
                bot.send_message(message.chat.id, f"[id:{user_admin[message.chat.id]}]\nЗдравствуйте, я модератор телеграм бота Studlife, чем могу быть полезен?", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.chat.id == 920781539 and (message.text == "!add" or message.text == "!remove"):
        if message.text == "!add":
            msg = bot.send_message(message.chat.id, "Введите id пользователя", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Отмена")))
            bot.register_next_step_handler(msg, add)
        else:
            msg = bot.send_message(message.chat.id, "Введите id пользователя",
                                   reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                       types.KeyboardButton("Отмена")))
            for i in admin_ids:
                bot.send_message(message.chat.id, str(i))
            bot.register_next_step_handler(msg, remove)
    if message.chat.id in admin_ids and message.chat.id in user_admin:
        if message.text == "Завершить диалог":
            bot.send_message(message.chat.id, "Вы завершили диалог!", reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(user_admin[message.chat.id], "Администратор завершил диалог!\nОбратиться снова - /ask", reply_markup=types.ReplyKeyboardRemove())
            del user_admin[user_admin[message.chat.id]]
            del user_admin[message.chat.id]
            print(user_admin)
            print("Диалог завершен со стороны админа!")
        else:
            bot.copy_message(user_admin[message.chat.id], message.chat.id, message.message_id)
    elif message.chat.id not in admin_ids and message.chat.id not in user_admin:
        bot.send_message(message.chat.id, "Обратиться за поддержкой - /ask")
    elif message.chat.id not in admin_ids and message.chat.id in user_admin:
        if message.text == "Завершить диалог":
            bot.send_message(message.chat.id, "Вы завершили диалог!", reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(user_admin[message.chat.id], "Пользователь завершил диалог!", reply_markup=types.ReplyKeyboardRemove())
            del user_admin[user_admin[message.chat.id]]
            del user_admin[message.chat.id]
            print(user_admin)
            print("Диалог завершен со стороны пользователя!")
        else:
            bot.copy_message(user_admin[message.chat.id], message.chat.id, message.message_id)
    else:
        if message.text != "!add" and message.text != "!remove":
            bot.send_message(message.chat.id, "К вам еще никто не обращался!")

def add(message):
    if message.text == "Отмена":
        bot.send_message(message.chat.id, "Отменено!", reply_markup=types.ReplyKeyboardRemove())
    else:
        admin_ids.append(int(message.text))
        bot.send_message(message.chat.id, "Добавлено!", reply_markup=types.ReplyKeyboardRemove())
    print(admin_ids)



def remove(message):
    if message.text == "Отмена":
        bot.send_message(message.chat.id, "Отменено!", reply_markup=types.ReplyKeyboardRemove())
    else:
        if int(message.text) in admin_ids:
            admin_ids.remove(int(message.text))
            bot.send_message(message.chat.id, "Удалено!", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id, "Нет такого юзера!", reply_markup=types.ReplyKeyboardRemove())
    print(admin_ids)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        time.sleep(15)


