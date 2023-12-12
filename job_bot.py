import time

from registration import *
from feed import *
from configs.config_job import *
from bd import *

# vacancy_resume = {20202602: [message_id: message.id, userid: @message.from_user.username]}



@job_bot.message_handler(commands=["start"])
def welcome(message):
    resumeRegistration = ResumeRegistration(data = get_resume(message.from_user.id))
    job_bot.send_message(message.chat.id, 'Добро пожаловать в бота "Стажировки для студентов"! 🚀🎓\n'
                                      'Здесь ты найдешь удобный и быстрый способ находить интересные и перспективные стажировки. Мы поможем тебе стартовать в карьере, предоставив доступ к разнообразным предложениям от ведущих компаний.\n'
                                      'Чтобы начать, выбери одну из опций в меню или введи ключевое слово, связанное с интересующей тебя областью. Мы постараемся сделать поиск стажировок максимально удобным и эффективным!\n'
                                      'Если у тебя есть вопросы или нужна помощь, не стесняйся обращаться. Удачи в поиске стажировки! 💼🌐')

    if resumeRegistration.name:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=resumeRegistration.name)
        markup.add(btn1)
        msg = job_bot.send_message(message.chat.id,
                       "Теперь давай начнем, для начала, как к тебе обращаться:", reply_markup=markup)
    else:
        msg = job_bot.send_message(message.chat.id,
                               "Теперь давай начнем, для начала, как к тебе обращаться:")
    job_bot.register_next_step_handler(msg, resumeRegistration.get_fio)


@job_bot.message_handler(commands=["ads"])
def ads(message):
    if message.chat.id in admin_list:
        msg = job_bot.send_message(message.chat.id, "Отправьте сообщение!")
        job_bot.register_next_step_handler(msg, add)


@job_bot.message_handler(commands=["add_vacancy"])
def add_vacancy(message):
    if message.chat.id in admin_list:
        vacancyRegistration = VacancyRegistration()
        msg = job_bot.send_message(message.chat.id, "Название компании!")
        job_bot.register_next_step_handler(msg, vacancyRegistration.get_fio)

@job_bot.message_handler(commands=["add_id", "remove_id"])
def answer(message):
    if message.chat.id in admin_list:
        if message.text == "/add_id":
            msg = job_bot.send_message(message.chat.id, "Введите id пользователя", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Отмена")))
            job_bot.register_next_step_handler(msg, add_id)
        else:
            msg = job_bot.send_message(message.chat.id, "Введите id пользователя",
                                   reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                       types.KeyboardButton("Отмена")))
            for i in admin_list:
                job_bot.send_message(message.chat.id, str(i))
            job_bot.register_next_step_handler(msg, remove_id)

@job_bot.message_handler(content_types=["text"])
def index(message):
    if message.text == "📞 Контакты":
        job_bot.send_message(message.chat.id, f"Если у вас есть вопросы или нужна помощь, не стесняйтесь обращаться:\n\n"
                                          f"Официальный канал: <a href='https://t.me/+S46mvD24xeFhZWIy'>Студлайф</a>\n"
                                          f"Поддержка: <a href='https://t.me/modersstudlifebot'>Модерация</a>\n\n"
                                          f"Наши администраторы всегда готовы помочь вам! 🚀📚🤝", parse_mode="HTML")

    elif message.text == "👥 Моя анкета":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text="Обновить анкету")
        btn2 = types.KeyboardButton(text="Смотреть анкеты")
        btn3 = types.KeyboardButton(text="Меню")
        markup.row(btn1, btn2).row(btn3)
        bd_resume = get_resume(message.from_user.id)
        msg = job_bot.send_message(message.chat.id, f"👥 Ваша Анкета резюме\n"
                                          f"👤 Меня зовут: {bd_resume[2]}\n"
                                          f"🏡 Живу в : {bd_resume[3]}\n"
                                          f"🔍 Обо мне: {bd_resume[4]}\n", reply_markup=markup)

        job_bot.register_next_step_handler(msg, resume)

    elif message.text == "🔍 Смотреть анкеты":
        data = get_resume(message.from_user.id)
        bd_job = feed_job(data[3])
        count = None
        if bd_job:
            for i in range(len(bd_job)):

                if bd_job[i][8] == 1:
                    count = i
                    break

            if count != None:
                jobFeed = JobFeed(count, data)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("❤")
                btn2 = types.KeyboardButton("👎")
                btn3 = types.KeyboardButton("💤")

                markup.row(btn1, btn2, btn3)

                msg = job_bot.send_message(message.chat.id, f"👥 Анкета Стажировки\n\n"
                                                        f"🏢 Название компании: {bd_job[count][1]}\n"
                                                        f"💼 Должность стажера: {bd_job[count][4]}\n"
                                                        f"🌟 Условия стажировки: {bd_job[count][6]}\n"
                                                        f"⏰ Обязанности: {bd_job[count][4]}\n"
                                                        f"💰 Зарплата (если предусмотрено): {bd_job[count][7]}", reply_markup=markup)
                job_bot.register_next_step_handler(msg, jobFeed.feed)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
                btn2 = types.KeyboardButton("👥 Моя анкета")
                btn4 = types.KeyboardButton("📞 Контакты")
                btn5 = types.KeyboardButton("📞 Оставить отзыв")

                markup.row(btn1, btn2).row(btn4, btn5)
                job_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2).row(btn4, btn5)
            job_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

    elif message.text == "📞 Оставить отзыв":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("❌ Отменить")

        markup.add(btn1)

        msg = job_bot.send_message(message.chat.id, "Нам очень важна обратная связь, поэтому, оставьте пожалуйста отзыв:",
                               reply_markup=markup)

        job_bot.register_next_step_handler(msg, feedback)

    else:
        job_bot.send_message(message.chat.id, "Нет такого варианта!")


def add(message):
    ids = get_id_job()
    print(len(ids))

    for id in ids:
        try:
            job_bot.copy_message(id[0], message.chat.id, message.message_id)
        except Exception as e:
            print(id[0], " Пользователь заблокировал бота!")
            print(e)


def feedback(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
    btn2 = types.KeyboardButton("👥 Моя анкета")
    btn4 = types.KeyboardButton("📞 Контакты")
    btn5 = types.KeyboardButton("📞 Оставить отзыв")

    markup.row(btn1, btn2).row(btn4, btn5)
    if message.text == "❌ Отменить":
        job_bot.send_message(message.chat.id, 'Добро пожаловать в бота "Стажировки для студентов"! 🚀🎓\n'
                                          'Здесь ты найдешь удобный и быстрый способ находить интересные и перспективные стажировки. Мы поможем тебе стартовать в карьере, предоставив доступ к разнообразным предложениям от ведущих компаний.\n'
                                          'Чтобы начать, выбери одну из опций в меню или введи ключевое слово, связанное с интересующей тебя областью. Мы постараемся сделать поиск стажировок максимально удобным и эффективным!\n'
                                          'Если у тебя есть вопросы или нужна помощь, не стесняйся обращаться. Удачи в поиске стажировки! 💼🌐',
                         reply_markup=markup)
    else:
        with open("reviews.txt", "a+", encoding="UTF-8") as f:
            f.write(str(message.from_user.username) + ":(" + message.text + ")\n")
        job_bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")
        job_bot.send_message(message.chat.id, 'Добро пожаловать в бота "Стажировки для студентов"! 🚀🎓\n'
                                          'Здесь ты найдешь удобный и быстрый способ находить интересные и перспективные стажировки. Мы поможем тебе стартовать в карьере, предоставив доступ к разнообразным предложениям от ведущих компаний.\n'
                                          'Чтобы начать, выбери одну из опций в меню или введи ключевое слово, связанное с интересующей тебя областью. Мы постараемся сделать поиск стажировок максимально удобным и эффективным!\n'
                                          'Если у тебя есть вопросы или нужна помощь, не стесняйся обращаться. Удачи в поиске стажировки! 💼🌐',
                         reply_markup=markup)


def reg(message):
    if message.text == "Регистрация":
        resumeRegistration = ResumeRegistration(data=get_resume(message.from_user.id))
        job_bot.send_message(message.chat.id, 'Добро пожаловать в бота "Стажировки для студентов"! 🚀🎓\n'
                                          'Здесь ты найдешь удобный и быстрый способ находить интересные и перспективные стажировки. Мы поможем тебе стартовать в карьере, предоставив доступ к разнообразным предложениям от ведущих компаний.\n'
                                          'Чтобы начать, выбери одну из опций в меню или введи ключевое слово, связанное с интересующей тебя областью. Мы постараемся сделать поиск стажировок максимально удобным и эффективным!\n'
                                          'Если у тебя есть вопросы или нужна помощь, не стесняйся обращаться. Удачи в поиске стажировки! 💼🌐')

        if resumeRegistration.name:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text=resumeRegistration.name)
            markup.add(btn1)
            msg = job_bot.send_message(message.chat.id,
                                   "Теперь давай начнем, для начала, как к тебе обращаться:", reply_markup=markup)
        else:
            msg = job_bot.send_message(message.chat.id,
                                   "Теперь давай начнем, для начала, как к тебе обращаться:")
        job_bot.register_next_step_handler(msg, resumeRegistration.get_fio)
    else:
        msg = job_bot.send_message(message.chat.id, "Чтобы снова смотреть анкета сначала зарегистрируйтесь")

        job_bot.register_next_step_handler(msg, reg)


def add_id(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
    btn2 = types.KeyboardButton("👥 Моя анкета")
    btn4 = types.KeyboardButton("📞 Контакты")
    btn5 = types.KeyboardButton("📞 Оставить отзыв")

    markup.row(btn1, btn2).row(btn4, btn5)
    if message.text == "Отмена":
        job_bot.send_message(message.chat.id, "Отменено!", reply_markup=markup)
    else:
        admin_list.append(int(message.text))
        job_bot.send_message(message.chat.id, "Добавлено!", reply_markup=markup)
    print(admin_list)


def remove_id(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
    btn2 = types.KeyboardButton("👥 Моя анкета")
    btn4 = types.KeyboardButton("📞 Контакты")
    btn5 = types.KeyboardButton("📞 Оставить отзыв")

    markup.row(btn1, btn2).row(btn4, btn5)
    if message.text == "Отмена":
        job_bot.send_message(message.chat.id, "Отменено!", reply_markup=markup)
    else:
        if int(message.text) in admin_list:
            admin_list.remove(int(message.text))
            job_bot.send_message(message.chat.id, "Удалено!", reply_markup=markup)
        else:
            job_bot.send_message(message.chat.id, "Нет такого юзера!", reply_markup=markup)
    print(admin_list)


def resume(message):
    if message.text == "Обновить анкету":
        resumeRegistration = ResumeRegistration(data = get_resume(message.from_user.id))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=resumeRegistration.name)
        markup.add(btn1)
        msg = job_bot.send_message(message.chat.id,
                               "Обновление данных:\n\nФИО:",
                               reply_markup=markup)

        job_bot.register_next_step_handler(msg, resumeRegistration.get_fio)

    elif message.text == "Смотреть анкеты":
        data = get_resume(message.from_user.id)
        bd_job = feed_job(data[3])
        count = None
        if bd_job:
            for i in range(len(bd_job)):

                if bd_job[i][8] == 1:
                    count = i
                    break

            if count != None:
                jobFeed = JobFeed(count, data)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("❤")
                btn2 = types.KeyboardButton("👎")
                btn3 = types.KeyboardButton("💤")

                markup.row(btn1, btn2, btn3)

                msg = job_bot.send_message(message.chat.id, f"👥 Анкета Стажировки\n\n"
                                                        f"🏢 Название компании: {bd_job[count][1]}\n"
                                                        f"💼 Должность стажера: {bd_job[count][3]}\n"
                                                        f"📋 Требования к стажеру: {bd_job[count][4]}\n"
                                                        f"🌟 Условия стажировки: {bd_job[count][6]}\n"
                                                        f"⏰ Обязанности: {bd_job[count][4]}\n"
                                                        f"💰 Зарплата (если предусмотрено): {bd_job[0][7]}", reply_markup=markup)
                job_bot.register_next_step_handler(msg, jobFeed.feed)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
                btn2 = types.KeyboardButton("👥 Моя анкета")
                btn4 = types.KeyboardButton("📞 Контакты")
                btn5 = types.KeyboardButton("📞 Оставить отзыв")

                markup.row(btn1, btn2).row(btn4, btn5)
                job_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2).row(btn4, btn5)
            job_bot.send_message(message.chat.id, "Анкет пока нет!", reply_markup=markup)

    elif message.text == "Меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
        btn2 = types.KeyboardButton("👥 Моя анкета")
        btn4 = types.KeyboardButton("📞 Контакты")
        btn5 = types.KeyboardButton("📞 Оставить отзыв")

        markup.row(btn1, btn2).row(btn4, btn5)
        job_bot.send_message(message.chat.id, 'Добро пожаловать в бота "Стажировки для студентов"! 🚀🎓\n'
                                          'Здесь ты найдешь удобный и быстрый способ находить интересные и перспективные стажировки. Мы поможем тебе стартовать в карьере, предоставив доступ к разнообразным предложениям от ведущих компаний.\n'
                                          'Чтобы начать, выбери одну из опций в меню или введи ключевое слово, связанное с интересующей тебя областью. Мы постараемся сделать поиск стажировок максимально удобным и эффективным!\n'
                                          'Если у тебя есть вопросы или нужна помощь, не стесняйся обращаться. Удачи в поиске стажировки! 💼🌐', reply_markup=markup)
    else:
        msg = job_bot.send_message(message.chat.id, "Нет такого варианта ответа!")
        job_bot.register_next_step_handler(msg, resume)


@job_bot.callback_query_handler(func=lambda call: True)
def like(call):
    if call.data == "like":
        for i in vacancy_resume:
            for j in range(len(vacancy_resume[i])):
                if call.message.text == vacancy_resume[i][j]["text"]:
                    job_bot.edit_message_text(f"Эта анкета удалена!", call.message.chat.id, call.message.message_id)
                    del_job(i, 0)
                    vacancy_resume[i].pop(j)
                    break
    elif call.data == "dislike":
        for i in vacancy_resume:
            for j in range(len(vacancy_resume[i])):
                if call.message.text == vacancy_resume[i][j]["text"]:
                    job_bot.edit_message_text(f"Вакансия остается!", call.message.chat.id, call.message.message_id)
                    vacancy_resume[i].pop(j)
                    break

while True:
    try:
        job_bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        time.sleep(15)
