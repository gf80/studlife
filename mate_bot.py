import time

from registration import *
from feed import *
from configs.config_mate import *
from bd import *


# users = {20202602: [message_id: message.id, userid: @message.from_user.username]}


@mate_bot.message_handler(commands=["start"])
def welcome(message):
    mateRegistration = MateRegistration(data = get_mate(message.from_user.id))
    mate_bot.send_message(message.chat.id, '🏡 Добро пожаловать в бота "Studlife Mate"! 🏡\n\n'
                                      'Если вы ищете надежных и симпатичных соседей для совместной аренды жилья, вы нашли правильное место. Наш бот поможет вам найти идеальных соседей, которые соответствуют вашим критериям и предпочтениям.\n\n'
                                      'Что вы можете делать с нашим ботом:\n'
                                      '🔍 Размещать анкеты и описания жилья, которое вы хотели бы сдать в аренду\n'
                                      '🧑‍🤝‍🧑 Искать соседей, чтобы совместно арендовать жилье и сэкономить на жилищных расходах.\n'
                                      '📝 Описывать себя и свои критерии по сожительству, чтобы найти подходящих соучасников.\n'
                                      '💬 Общаться с потенциальными соседями и договариваться о деталях аренды.')
    mate_bot.send_message(message.chat.id, "❗️Помни, что в интернете люди могут выдавать себя за других.\n"
                                      "Бот не запрашивает личные данные и не идентифицирует пользователей по паспортным данным. \n"
                                      "Продолжая ты соглашаешься с использованием бота на свой страх и риск.")

    if mateRegistration.name:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=mateRegistration.name)
        markup.add(btn1)
        msg = mate_bot.send_message(message.chat.id,
                       "Теперь давай начнем, для начала, как к тебе обращаться:", reply_markup=markup)
    else:
        msg = mate_bot.send_message(message.chat.id,
                               "Теперь давай начнем, для начала, как к тебе обращаться:")
    mate_bot.register_next_step_handler(msg, mateRegistration.get_fio)

@mate_bot.message_handler(commands=["ads"])
def ads(message):
    if message.chat.id == 920781539:
        msg = mate_bot.send_message(920781539, "Отправьте сообщение!")
        mate_bot.register_next_step_handler(msg, add)

def add(message):
    ids = get_id_mate()
    print(len(ids))

    for id in ids:
        try:
            mate_bot.copy_message(id[0], 920781539, message.message_id)
        except Exception as e:
            print(id[0], " Пользователь заблокировал бота!")
            print(e)


@mate_bot.message_handler(content_types=["text"])
def index(message):
    if message.text == "📞 Контакты":
        mate_bot.send_message(message.chat.id, f"Если у вас есть вопросы или нужна помощь, не стесняйтесь обращаться:\n\n"
                                          f"Официальный канал: <a href='https://t.me/+S46mvD24xeFhZWIy'>Студлайф</a>\n"
                                          f"Поддержка: <a href='https://t.me/modersstudlifebot'>Модерация</a>\n\n"
                                          f"Наши администраторы всегда готовы помочь вам! 🚀📚🤝", parse_mode="HTML")

    elif message.text == "👥 Моя анкета":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text="Обновить анкету")
        btn2 = types.KeyboardButton(text="Смотреть анкеты")
        btn3 = types.KeyboardButton(text="Меню")
        markup.row(btn1, btn2).row(btn3)
        bd_mate = get_mate(message.from_user.id)
        msg = mate_bot.send_message(message.chat.id, f"👥 Ваша Анкета Соседа\n"
                                          f"👤 Меня зовут: {bd_mate[1]}\n"
                                          f"🏡 Ищу соседа в: {bd_mate[3]}\n"
                                          f"📅 Мой возраст: {bd_mate[4]}\n"
                                          f"💰 Бюджет: {bd_mate[5]}\n"
                                          f"🔍 Обо мне: {bd_mate[7]}\n"
                                          f"🔍 О тебе: {bd_mate[8]}", reply_markup=markup)

        mate_bot.register_next_step_handler(msg, mate)

    elif message.text == "🔍 Смотреть анкеты":
        data = get_mate(message.from_user.id)
        bd_mate = feed_mate(data[0], data[3], data[6], data[9])
        count = None
        if bd_mate:
            for i in range(len(bd_mate)):

                if bd_mate[i][10] == 1:
                    count = i
                    break

            if count != None:
                mateFeed = MateFeed(count, data)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("❤")
                btn2 = types.KeyboardButton("👎")
                btn3 = types.KeyboardButton("💤")

                markup.row(btn1, btn2, btn3)

                msg = mate_bot.send_message(message.chat.id, f"👥 Анкета Соседа\n\n"
                                                        f"👤 Меня зовут: {bd_mate[count][1]}\n"
                                                        f"🏡 Ищу соседа в: {bd_mate[count][3]}\n"
                                                        f"📅 Мой возраст: {bd_mate[count][4]}\n"
                                                        f"💰 Бюджет: {bd_mate[count][5]}\n"
                                                        f"🔍 Обо мне: {bd_mate[count][7]}\n"
                                                        f"🔍 О тебе: {bd_mate[count][8]}", reply_markup=markup)
                mate_bot.register_next_step_handler(msg, mateFeed.feed)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
                btn2 = types.KeyboardButton("👥 Моя анкета")
                btn3 = types.KeyboardButton("❌ Удалить анкету")
                btn4 = types.KeyboardButton("📞 Контакты")
                btn5 = types.KeyboardButton("📞 Оставить отзыв")

                markup.row(btn1, btn2, btn3).row(btn4, btn5)
                mate_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn3 = types.KeyboardButton("❌ Удалить анкету")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2, btn3).row(btn4, btn5)
            mate_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

    elif message.text == "❌ Удалить анкету":
        del_mate(message.from_user.id, 0)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Регистрация")
        markup.add(btn1)
        msg = mate_bot.send_message(message.chat.id, "Ваша анкета удалена!", reply_markup=markup)
        mate_bot.register_next_step_handler(msg, reg)

    elif message.text == "📞 Оставить отзыв":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("❌ Отменить")

        markup.add(btn1)

        msg = mate_bot.send_message(message.chat.id, "Нам очень важна обратная связь, поэтому, оставьте пожалуйста отзыв:",
                               reply_markup=markup)

        mate_bot.register_next_step_handler(msg, feedback)

    else:
        mate_bot.send_message(message.chat.id, "Нет такого варианта!")


def feedback(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
    btn2 = types.KeyboardButton("👥 Моя анкета")
    btn3 = types.KeyboardButton("❌ Удалить анкету")
    btn4 = types.KeyboardButton("📞 Контакты")
    btn5 = types.KeyboardButton("📞 Оставить отзыв")

    markup.row(btn1, btn2, btn3).row(btn4, btn5)
    if message.text == "❌ Отменить":

        mate_bot.send_message(message.chat.id, '🏡 Добро пожаловать в бота "Studlife Mate"! 🏡\n\n'
                                          'Если вы ищете надежных и симпатичных соседей для совместной аренды жилья, вы нашли правильное место. Наш бот поможет вам найти идеальных соседей, которые соответствуют вашим критериям и предпочтениям.\n\n'
                                          'Что вы можете делать с нашим ботом:\n'
                                          '🔍 Размещать анкеты и описания жилья, которое вы хотели бы сдать в аренду\n'
                                          '🧑‍🤝‍🧑 Искать соседей, чтобы совместно арендовать жилье и сэкономить на жилищных расходах.\n'
                                          '📝 Описывать себя и свои критерии по сожительству, чтобы найти подходящих соучасников.\n'
                                          '💬 Общаться с потенциальными соседями и договариваться о деталях аренды.',
                         reply_markup=markup)
    else:
        with open("reviews.txt", "a+", encoding="UTF-8") as f:
            f.write(str(message.from_user.username) + ":(" + message.text + ")\n")
        mate_bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")
        mate_bot.send_message(message.chat.id, '🏡 Добро пожаловать в бота "Studlife Mate"! 🏡\n\n'
                                          'Если вы ищете надежных и симпатичных соседей для совместной аренды жилья, вы нашли правильное место. Наш бот поможет вам найти идеальных соседей, которые соответствуют вашим критериям и предпочтениям.\n\n'
                                          'Что вы можете делать с нашим ботом:\n'
                                          '🔍 Размещать анкеты и описания жилья, которое вы хотели бы сдать в аренду\n'
                                          '🧑‍🤝‍🧑 Искать соседей, чтобы совместно арендовать жилье и сэкономить на жилищных расходах.\n'
                                          '📝 Описывать себя и свои критерии по сожительству, чтобы найти подходящих соучасников.\n'
                                          '💬 Общаться с потенциальными соседями и договариваться о деталях аренды.',
                         reply_markup=markup)


def reg(message):
    if message.text == "Регистрация":
        mateRegistration = MateRegistration(data = get_mate(message.from_user.id))
        if mateRegistration.name:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text=mateRegistration.name)
            markup.add(btn1)
            msg = mate_bot.send_message(message.chat.id,
                                   "Для завершения регистрации, пожалуйста, предоставьте следующие данные:\n\nФИО:",
                                   reply_markup=markup)
        else:
            msg = mate_bot.send_message(message.chat.id,
                                   "Для завершения регистрации, пожалуйста, предоставьте следующие данные:\n\nФИО:")
        mate_bot.register_next_step_handler(msg, mateRegistration.get_fio)
    else:
        msg = mate_bot.send_message(message.chat.id, "Чтобы снова смотреть анкета сначала зарегистрируйтесь")

        mate_bot.register_next_step_handler(msg, reg)

def mate(message):
    if message.text == "Обновить анкету":
        mateRegistration = MateRegistration(data = get_mate(message.from_user.id))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=mateRegistration.name)
        markup.add(btn1)
        msg = mate_bot.send_message(message.chat.id,
                               "Обновление данных:\n\nФИО:",
                               reply_markup=markup)

        mate_bot.register_next_step_handler(msg, mateRegistration.get_fio)

    elif message.text == "Смотреть анкеты":
        data = get_mate(message.from_user.id)
        bd_mate = feed_mate(data[0], data[3], data[6], data[9])
        count = None
        if bd_mate:
            for i in range(len(bd_mate)):

                if bd_mate[i][10] == 1:
                    count = i
                    break

            if count != None:
                mateFeed = MateFeed(count, data)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("❤")
                btn2 = types.KeyboardButton("👎")
                btn3 = types.KeyboardButton("💤")

                markup.row(btn1, btn2, btn3)

                msg = mate_bot.send_message(message.chat.id, f"👥 Анкета Соседа\n\n"
                                                        f"👤 Меня зовут: {bd_mate[count][1]}\n"
                                                        f"🏡 Ищу соседа в: {bd_mate[count][3]}\n"
                                                        f"📅 Мой возраст: {bd_mate[count][4]}\n"
                                                        f"💰 Бюджет: {bd_mate[count][5]}\n"
                                                        f"🔍 Обо мне: {bd_mate[count][7]}\n"
                                                        f"🔍 О тебе: {bd_mate[count][8]}", reply_markup=markup)
                mate_bot.register_next_step_handler(msg, mateFeed.feed)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
                btn2 = types.KeyboardButton("👥 Моя анкета")
                btn3 = types.KeyboardButton("❌ Удалить анкету")
                btn4 = types.KeyboardButton("📞 Контакты")
                btn5 = types.KeyboardButton("📞 Оставить отзыв")

                markup.row(btn1, btn2, btn3).row(btn4, btn5)
                mate_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn3 = types.KeyboardButton("❌ Удалить анкету")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2, btn3).row(btn4, btn5)
            mate_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

    elif message.text == "Меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
        btn2 = types.KeyboardButton("👥 Моя анкета")
        btn3 = types.KeyboardButton("❌ Удалить анкету")
        btn4 = types.KeyboardButton("📞 Контакты")
        btn5 = types.KeyboardButton("📞 Оставить отзыв")

        markup.row(btn1, btn2, btn3).row(btn4, btn5)
        mate_bot.send_message(message.chat.id, '🏡 Добро пожаловать в бота "Studlife Mate"! 🏡\n\n'
                                      'Если вы ищете надежных и симпатичных соседей для совместной аренды жилья, вы нашли правильное место. Наш бот поможет вам найти идеальных соседей, которые соответствуют вашим критериям и предпочтениям.\n\n'
                                      'Что вы можете делать с нашим ботом:\n'
                                      '🔍 Размещать анкеты и описания жилья, которое вы хотели бы сдать в аренду\n'
                                      '🧑‍🤝‍🧑 Искать соседей, чтобы совместно арендовать жилье и сэкономить на жилищных расходах.\n'
                                      '📝 Описывать себя и свои критерии по сожительству, чтобы найти подходящих соучасников.\n'
                                      '💬 Общаться с потенциальными соседями и договариваться о деталях аренды.', reply_markup=markup)
    else:
        msg = mate_bot.send_message(message.chat.id, "Нет такого варианта ответа!")
        mate_bot.register_next_step_handler(msg, mate)


@mate_bot.callback_query_handler(func=lambda call: True)
def like(call):
    if call.data == "like":
        for i in range(len(users[call.from_user.id])):
            if call.message.text == users[call.from_user.id][i]["text"]:
                mate_bot.edit_message_text(f"Это взаимная симпатия!\nПереходите в лс и договаривайтесь о встрече\n\n{users[call.from_user.id][i]['username']}", call.message.chat.id, call.message.message_id)
                users[call.from_user.id].pop(i)
    elif call.data == "dislike":
        for i in range(len(users[call.from_user.id])):
            if call.message.text == users[call.from_user.id][i]["text"]:
                mate_bot.edit_message_text(f"Надеемся, что вы найдете еще кого-то", call.message.chat.id, call.message.message_id)
                users[call.from_user.id].pop(i)


while True:
    try:
        mate_bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        time.sleep(15)