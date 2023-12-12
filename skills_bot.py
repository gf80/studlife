import time

from registration import *
from feed import *
from configs.config_skills import *
from bd import *


# skills_users = {20202602: [message_id: message.id, userid: @message.from_user.username]}


@skills_bot.message_handler(commands=["start"])
def welcome(message):
    skillsRegistration = SkillsRegistration(data = get_skills(message.from_user.id))
    skills_bot.send_message(message.chat.id, 'Добро пожаловать в бот "Обмен навыками"! 🔄🤝\n'
                                             'Здесь ты сможешь найти партнеров для обмена навыками и знаний. Обучение становится увлекательным, когда есть кто-то, с кем можно делиться опытом и учиться новому!\n'
                                             'Выбери раздел в меню или введи ключевое слово, чтобы начать. Мы постараемся подобрать для тебя идеальных партнеров, с которыми обучение станет интересным и продуктивным!\n'
                                             'Если у тебя возникнут вопросы или нужна помощь, не стесняйся обращаться. Удачи в обмене навыками! 🚀📚🔁')
    skills_bot.send_message(message.chat.id, "❗️Помни, что в интернете люди могут выдавать себя за других.\n"
                                      "Бот не запрашивает личные данные и не идентифицирует пользователей по паспортным данным. \n"
                                      "Продолжая ты соглашаешься с использованием бота на свой страх и риск.")

    if skillsRegistration.name:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=skillsRegistration.name)
        markup.add(btn1)
        msg = skills_bot.send_message(message.chat.id,
                       "Теперь давай начнем, для начала, как к тебе обращаться:", reply_markup=markup)
    else:
        msg = skills_bot.send_message(message.chat.id,
                               "Теперь давай начнем, для начала, как к тебе обращаться:")
    skills_bot.register_next_step_handler(msg, skillsRegistration.get_fio)

@skills_bot.message_handler(commands=["ads"])
def ads(message):
    if message.chat.id == 920781539:
        msg = skills_bot.send_message(920781539, "Отправьте сообщение!")
        skills_bot.register_next_step_handler(msg, add)

def add(message):
    ids = get_id_skills()
    print(len(ids))

    for id in ids:
        try:
            skills_bot.copy_message(id[0], 920781539, message.message_id)
        except Exception as e:
            print(id[0], " Пользователь заблокировал бота!")
            print(e)


@skills_bot.message_handler(content_types=["text"])
def index(message):
    if message.text == "📞 Контакты":
        skills_bot.send_message(message.chat.id, f"Если у вас есть вопросы или нужна помощь, не стесняйтесь обращаться:\n\n"
                                          f"Официальный канал: <a href='https://t.me/+S46mvD24xeFhZWIy'>Студлайф</a>\n"
                                          f"Поддержка: <a href='https://t.me/modersstudlifebot'>Модерация</a>\n\n"
                                          f"Наши администраторы всегда готовы помочь вам! 🚀📚🤝", parse_mode="HTML")

    elif message.text == "👥 Моя анкета":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text="Обновить анкету")
        btn2 = types.KeyboardButton(text="Смотреть анкеты")
        btn3 = types.KeyboardButton(text="Меню")
        markup.row(btn1, btn2).row(btn3)
        bd_skills = get_skills(message.from_user.id)
        msg = skills_bot.send_message(message.chat.id, f"👥 Ваша Анкета Соседа\n"
                                          f"👤 Меня зовут: {bd_skills[1]}\n"
                                          f"🏡 Ищу человека в: {bd_skills[3]}\n"
                                          f"📅 Мой возраст: {bd_skills[4]}\n"
                                          f"🔍 Обо мне: {bd_skills[6]}\n"
                                          f"🔍 О тебе: {bd_skills[7]}", reply_markup=markup)

        skills_bot.register_next_step_handler(msg, skills)

    elif message.text == "🔍 Смотреть анкеты":
        data = get_skills(message.from_user.id)
        bd_skills = feed_skills(data[0], data[3], data[6], data[9])
        count = None
        if bd_skills:
            for i in range(len(bd_skills)):

                if bd_skills[i][10] == 1:
                    count = i
                    break

            if count != None:
                skillsFeed = SkillsFeed(count, data)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("❤")
                btn2 = types.KeyboardButton("👎")
                btn3 = types.KeyboardButton("💤")

                markup.row(btn1, btn2, btn3)

                msg = skills_bot.send_message(message.chat.id, f"👥 Анкета Соседа\n\n"
                                                        f"👤 Меня зовут: {bd_skills[count][1]}\n"
                                                        f"🏡 Ищу человека в: {bd_skills[count][3]}\n"
                                                        f"📅 Мой возраст: {bd_skills[count][4]}\n"
                                                        f"🔍 Обо мне: {bd_skills[count][6]}\n"
                                                        f"🔍 О тебе: {bd_skills[count][7]}", reply_markup=markup)
                skills_bot.register_next_step_handler(msg, skillsFeed.feed)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
                btn2 = types.KeyboardButton("👥 Моя анкета")
                btn3 = types.KeyboardButton("❌ Удалить анкету")
                btn4 = types.KeyboardButton("📞 Контакты")
                btn5 = types.KeyboardButton("📞 Оставить отзыв")

                markup.row(btn1, btn2, btn3).row(btn4, btn5)
                skills_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn3 = types.KeyboardButton("❌ Удалить анкету")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2, btn3).row(btn4, btn5)
            skills_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

    elif message.text == "❌ Удалить анкету":
        del_skills(message.from_user.id, 0)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Регистрация")
        markup.add(btn1)
        msg = skills_bot.send_message(message.chat.id, "Ваша анкета удалена!", reply_markup=markup)
        skills_bot.register_next_step_handler(msg, reg)

    elif message.text == "📞 Оставить отзыв":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("❌ Отменить")

        markup.add(btn1)

        msg = skills_bot.send_message(message.chat.id, "Нам очень важна обратная связь, поэтому, оставьте пожалуйста отзыв:",
                               reply_markup=markup)

        skills_bot.register_next_step_handler(msg, feedback)

    else:
        skills_bot.send_message(message.chat.id, "Нет такого варианта!")


def feedback(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
    btn2 = types.KeyboardButton("👥 Моя анкета")
    btn3 = types.KeyboardButton("❌ Удалить анкету")
    btn4 = types.KeyboardButton("📞 Контакты")
    btn5 = types.KeyboardButton("📞 Оставить отзыв")

    markup.row(btn1, btn2, btn3).row(btn4, btn5)
    if message.text == "❌ Отменить":

        skills_bot.send_message(message.chat.id, 'Добро пожаловать в бот "Обмен навыками"! 🔄🤝\n'
                                             'Здесь ты сможешь найти партнеров для обмена навыками и знаний. Обучение становится увлекательным, когда есть кто-то, с кем можно делиться опытом и учиться новому!\n'
                                             'Выбери раздел в меню или введи ключевое слово, чтобы начать. Мы постараемся подобрать для тебя идеальных партнеров, с которыми обучение станет интересным и продуктивным!\n'
                                             'Если у тебя возникнут вопросы или нужна помощь, не стесняйся обращаться. Удачи в обмене навыками! 🚀📚🔁',
                         reply_markup=markup)
    else:
        with open("reviews.txt", "a+", encoding="UTF-8") as f:
            f.write(str(message.from_user.username) + ":(" + message.text + ")\n")
        skills_bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")
        skills_bot.send_message(message.chat.id, 'Добро пожаловать в бот "Обмен навыками"! 🔄🤝\n'
                                             'Здесь ты сможешь найти партнеров для обмена навыками и знаний. Обучение становится увлекательным, когда есть кто-то, с кем можно делиться опытом и учиться новому!\n'
                                             'Выбери раздел в меню или введи ключевое слово, чтобы начать. Мы постараемся подобрать для тебя идеальных партнеров, с которыми обучение станет интересным и продуктивным!\n'
                                             'Если у тебя возникнут вопросы или нужна помощь, не стесняйся обращаться. Удачи в обмене навыками! 🚀📚🔁',
                         reply_markup=markup)


def reg(message):
    if message.text == "Регистрация":
        skillsRegistration = SkillsRegistration(data = get_skills(message.from_user.id))
        if skillsRegistration.name:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text=skillsRegistration.name)
            markup.add(btn1)
            msg = skills_bot.send_message(message.chat.id,
                                   "Для завершения регистрации, пожалуйста, предоставьте следующие данные:\n\nФИО:",
                                   reply_markup=markup)
        else:
            msg = skills_bot.send_message(message.chat.id,
                                   "Для завершения регистрации, пожалуйста, предоставьте следующие данные:\n\nФИО:")
        skills_bot.register_next_step_handler(msg, skillsRegistration.get_fio)
    else:
        msg = skills_bot.send_message(message.chat.id, "Чтобы снова смотреть анкета сначала зарегистрируйтесь")

        skills_bot.register_next_step_handler(msg, reg)

def skills(message):
    if message.text == "Обновить анкету":
        skillsRegistration = SkillsRegistration(data = get_skills(message.from_user.id))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=skillsRegistration.name)
        markup.add(btn1)
        msg = skills_bot.send_message(message.chat.id,
                               "Обновление данных:\n\nФИО:",
                               reply_markup=markup)

        skills_bot.register_next_step_handler(msg, skillsRegistration.get_fio)

    elif message.text == "Смотреть анкеты":
        data = get_skills(message.from_user.id)
        bd_skills = feed_skills(data[0], data[3], data[5], data[8])
        count = None
        if bd_skills:
            for i in range(len(bd_skills)):

                if bd_skills[i][9] == 1:
                    count = i
                    break

            if count != None:
                skillsFeed = SkillsFeed(count, data)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("❤")
                btn2 = types.KeyboardButton("👎")
                btn3 = types.KeyboardButton("💤")

                markup.row(btn1, btn2, btn3)

                msg = skills_bot.send_message(message.chat.id, f"👥 Анкета Соседа\n\n"
                                                        f"👤 Меня зовут: {bd_skills[count][1]}\n"
                                                        f"🏡 Ищу соседа в: {bd_skills[count][3]}\n"
                                                        f"📅 Мой возраст: {bd_skills[count][4]}\n"
                                                        f"🔍 Обо мне: {bd_skills[count][6]}\n"
                                                        f"🔍 О тебе: {bd_skills[count][7]}", reply_markup=markup)
                skills_bot.register_next_step_handler(msg, skillsFeed.feed)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
                btn2 = types.KeyboardButton("👥 Моя анкета")
                btn3 = types.KeyboardButton("❌ Удалить анкету")
                btn4 = types.KeyboardButton("📞 Контакты")
                btn5 = types.KeyboardButton("📞 Оставить отзыв")

                markup.row(btn1, btn2, btn3).row(btn4, btn5)
                skills_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn3 = types.KeyboardButton("❌ Удалить анкету")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2, btn3).row(btn4, btn5)
            skills_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

    elif message.text == "Меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
        btn2 = types.KeyboardButton("👥 Моя анкета")
        btn3 = types.KeyboardButton("❌ Удалить анкету")
        btn4 = types.KeyboardButton("📞 Контакты")
        btn5 = types.KeyboardButton("📞 Оставить отзыв")

        markup.row(btn1, btn2, btn3).row(btn4, btn5)
        skills_bot.send_message(message.chat.id, '🏡 Добро пожаловать в бота "Studlife Skills"! 🏡\n\n'
                                      'Если вы ищете надежных и симпатичных соседей для совместной аренды жилья, вы нашли правильное место. Наш бот поможет вам найти идеальных соседей, которые соответствуют вашим критериям и предпочтениям.\n\n'
                                      'Что вы можете делать с нашим ботом:\n'
                                      '🔍 Размещать анкеты и описания жилья, которое вы хотели бы сдать в аренду\n'
                                      '🧑‍🤝‍🧑 Искать соседей, чтобы совместно арендовать жилье и сэкономить на жилищных расходах.\n'
                                      '📝 Описывать себя и свои критерии по сожительству, чтобы найти подходящих соучасников.\n'
                                      '💬 Общаться с потенциальными соседями и договариваться о деталях аренды.', reply_markup=markup)
    else:
        msg = skills_bot.send_message(message.chat.id, "Нет такого варианта ответа!")
        skills_bot.register_next_step_handler(msg, skills)


@skills_bot.callback_query_handler(func=lambda call: True)
def like(call):
    if call.data == "like":
        for i in range(len(skills_users[call.from_user.id])):
            if call.message.text == skills_users[call.from_user.id][i]["text"]:
                skills_bot.edit_message_text(f"Это взаимная симпатия!\nПереходите в лс и договаривайтесь о встрече\n\n{skills_users[call.from_user.id][i]['username']}", call.message.chat.id, call.message.message_id)
                skills_users[call.from_user.id].pop(i)
    elif call.data == "dislike":
        for i in range(len(skills_users[call.from_user.id])):
            if call.message.text == skills_users[call.from_user.id][i]["text"]:
                skills_bot.edit_message_text(f"Надеемся, что вы найдете еще кого-то", call.message.chat.id, call.message.message_id)
                skills_users[call.from_user.id].pop(i)


while True:
    try:
        skills_bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        time.sleep(15)
