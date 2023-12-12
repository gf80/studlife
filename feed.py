import random

from configs.config_mate import *
from bd import *
from telebot import types
from configs.config_job import *
from configs.config_skills import *

class MateFeed:
    def __init__(self, count, data):
        self.count = count
        self.data = data
        self.ads_count = 0

    def feed(self, message):
        bd_mate = feed_mate(self.data[0], self.data[3], self.data[6], self.data[9])
        flag = True
        is_count = True

        if message.chat.id in users:
            if len(users[message.chat.id]) > 0:
                markup = types.InlineKeyboardMarkup()

                btn1 = types.InlineKeyboardButton("Лайк", callback_data="like")
                btn2 = types.InlineKeyboardButton("Дизлайк", callback_data="dislike")

                markup.add(btn1)
                markup.add(btn2)

                for i in range(len(users[message.chat.id])):
                    mate_bot.send_message(message.chat.id, text=users[message.chat.id][i]["text"], reply_markup=markup)
                msg = mate_bot.send_message(message.chat.id, "Ответьте на сообщения!", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Окей")))
                mate_bot.register_next_step_handler(msg, self.feed)
                return

        if message.text == "Окей":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("❤")
            btn2 = types.KeyboardButton("👎")
            btn3 = types.KeyboardButton("💤")

            markup.row(btn1, btn2, btn3)

            msg = mate_bot.send_message(message.chat.id, f"👥 Анкета Соседа\n\n"
                                                    f"👤 Меня зовут: {bd_mate[self.count][1]}\n"
                                                    f"🏡 Ищу соседа в: {bd_mate[self.count][3]}\n"
                                                    f"📅 Мой возраст: {bd_mate[self.count][4]}\n"
                                                    f"💰 Бюджет: {bd_mate[self.count][5]}\n"
                                                    f"🔍 Обо мне: {bd_mate[self.count][7]}\n"
                                                    f"🔍 О тебе: {bd_mate[self.count][8]}", reply_markup=markup)
            mate_bot.register_next_step_handler(msg, self.feed)
            return

        self.ads_count += 1

        if self.ads_count > 30:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn = types.KeyboardButton("Окей")
            markup.add(btn)

            msg = mate_bot.send_message(message.chat.id, "Пожалуйста, подпишитесь на наш основной канал: "
                                                    "<a href='https://t.me/+S46mvD24xeFhZWIy'>Студлайф</a>\n"
                                                    "В нем много интересной информации и другие полезные микросервисы для вас\n\n"
                                                    "С уважением команда Studlife", parse_mode="HTML",
                                   reply_markup=markup)
            mate_bot.register_next_step_handler(msg, self.feed_after)
            self.ads_count = 0
            return

        self.count_pred = self.count

        for i in range(self.count + 1, len(bd_mate)):
            if bd_mate[i][10] == 1:
                self.count = i
                print(self.count)
                flag = False
                is_count = False
                break

        if flag:
            for i in range(len(bd_mate)):
                if bd_mate[i][10] == 1:
                    is_count = False
                    self.count_pred = self.count
                    self.count = i
                    break

        if is_count or len(bd_mate) == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn3 = types.KeyboardButton("❌ Удалить анкету")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2, btn3).row(btn4, btn5)

            mate_bot.send_message(message.chat.id, "Анкет нет!", reply_markup=markup)

        else:
            if message.text == "👎":
                msg = mate_bot.send_message(message.chat.id, f"👥 Анкета Соседа\n\n"
                                                        f"👤 Меня зовут: {bd_mate[self.count][1]}\n"
                                                        f"🏡 Ищу соседа в: {bd_mate[self.count][3]}\n"
                                                        f"📅 Мой возраст: {bd_mate[self.count][4]}\n"
                                                        f"💰 Бюджет: {bd_mate[self.count][5]}\n"
                                                        f"🔍 Обо мне: {bd_mate[self.count][7]}\n"
                                                        f"🔍 О тебе: {bd_mate[self.count][8]}")
                mate_bot.register_next_step_handler(msg, self.feed)

            elif message.text == "❤":
                print(f"{self.data[1]} лайкнул {bd_mate[self.count_pred][1]}")

                if bd_mate[self.count_pred][0] in users:
                    if f'@{message.from_user.username}' in [i["username"] for i in
                                                            users[bd_mate[self.count_pred][0]]]:
                        mate_bot.send_message(message.chat.id, "Вы уже лайкнули этого пользователя!\nВидно он еще не ответил!")

                    else:
                        users[bd_mate[self.count - 1][0]].append({"username": f'@{message.from_user.username}',
                                                                  "text": f"{self.data[1]} лайнкул/а вашу анкету\n\n"
                                                                          f"👤 Меня зовут: {self.data[1]}\n"
                                                                          f"🏡 Ищу соседа в: {self.data[3]}\n"
                                                                          f"📅 Мой возраст: {self.data[4]}\n"
                                                                          f"💰 Бюджет: {self.data[5]}\n"
                                                                          f"🔍 Обо мне: {self.data[7]}\n"
                                                                          f"🔍 О тебе: {self.data[8]}"})
                else:
                    users[bd_mate[self.count_pred][0]] = [{"username": f'@{message.from_user.username}',
                                                           "text": f"{self.data[1]} лайнкул/а вашу анкету\n\n"
                                                                   f"👤 Меня зовут: {self.data[1]}\n"
                                                                   f"🏡 Ищу соседа в: {self.data[3]}\n"
                                                                   f"📅 Мой возраст: {self.data[4]}\n"
                                                                   f"💰 Бюджет: {self.data[5]}\n"
                                                                   f"🔍 Обо мне: {self.data[7]}\n"
                                                                   f"🔍 О тебе: {self.data[8]}"}]
                msg = mate_bot.send_message(message.chat.id, f"👥 Анкета Соседа\n\n"
                                                        f"👤 Меня зовут: {bd_mate[self.count][1]}\n"
                                                        f"🏡 Ищу соседа в: {bd_mate[self.count][3]}\n"
                                                        f"📅 Мой возраст: {bd_mate[self.count][4]}\n"
                                                        f"💰 Бюджет: {bd_mate[self.count][5]}\n"
                                                        f"🔍 Обо мне: {bd_mate[self.count][7]}\n"
                                                        f"🔍 О тебе: {bd_mate[self.count][8]}")

                mate_bot.register_next_step_handler(msg, self.feed)

            elif message.text == "💤":
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
                                                  '💬 Общаться с потенциальными соседями и договариваться о деталях аренды.',
                                 reply_markup=markup)

    def feed_after(self, message):
        bd_mate = feed_mate(self.data[0], self.data[3], self.data[6], self.data[9])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("❤")
        btn2 = types.KeyboardButton("👎")
        btn3 = types.KeyboardButton("💤")

        markup.row(btn1, btn2, btn3)

        msg = mate_bot.send_message(message.chat.id, f"👥 Анкета Соседа\n\n"
                                                f"👤 Меня зовут: {bd_mate[self.count][1]}\n"
                                                f"🏡 Ищу соседа в: {bd_mate[self.count][3]}\n"
                                                f"📅 Мой возраст: {bd_mate[self.count][4]}\n"
                                                f"💰 Бюджет: {bd_mate[self.count][5]}\n"
                                                f"🔍 Обо мне: {bd_mate[self.count][7]}\n"
                                                f"🔍 О тебе: {bd_mate[self.count][8]}", reply_markup=markup)
        mate_bot.register_next_step_handler(msg, self.feed)


class JobFeed:
    def __init__(self, count, data):
        self.count = count
        self.data = data
        self.ads_count = 0

    def feed(self, message):
        bd_job = feed_job(self.data[3]) # Получаем анкеты по совместительству города
        flag = True
        is_count = True

        if message.text == "Окей":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("❤")
            btn2 = types.KeyboardButton("👎")
            btn3 = types.KeyboardButton("💤")

            markup.row(btn1, btn2, btn3)

            msg = job_bot.send_message(message.chat.id, f"👥 Анкета Стажировки\n\n"
                                                      f"🏢 Название компании: {bd_job[self.count][1]}\n"
                                                      f"💼 Должность стажера: {bd_job[self.count][3]}\n"
                                                      f"📋 Требования к стажеру: {bd_job[self.count][4]}\n"
                                                      f"🌟 Условия стажировки: {bd_job[self.count][6]}\n"
                                                      f"⏰ Обязанности: {bd_job[self.count][4]}\n"
                                                      f"💰 Зарплата (если предусмотрено): {bd_job[self.count][7]}", reply_markup=markup)

            job_bot.register_next_step_handler(msg, self.feed)
            return

        self.ads_count += 1

        if self.ads_count > 30:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn = types.KeyboardButton("Окей")
            markup.add(btn)

            msg = job_bot.send_message(message.chat.id, "Пожалуйста, подпишитесь на наш основной канал: "
                                                    "<a href='https://t.me/+S46mvD24xeFhZWIy'>Студлайф</a>\n"
                                                    "В нем много интересной информации и другие полезные микросервисы для вас\n\n"
                                                    "С уважением команда Studlife", parse_mode="HTML",
                                   reply_markup=markup)
            job_bot.register_next_step_handler(msg, self.feed_after)
            self.ads_count = 0
            return

        self.count_pred = self.count
        # Ищем анкету
        for i in range(self.count + 1, len(bd_job)):
            if bd_job[i][8] == 1:
                self.count = i
                print(self.count)
                flag = False
                is_count = False
                break

        if flag:
            for i in range(len(bd_job)):
                if bd_job[i][8] == 1:
                    is_count = False
                    self.count_pred = self.count
                    self.count = i
                    break

        if is_count or len(bd_job) == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn3 = types.KeyboardButton("❌ Удалить анкету")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2, btn3).row(btn4, btn5)

            job_bot.send_message(message.chat.id, "Анкет нет!", reply_markup=markup)

        else:
            if message.text == "👎":
                msg = job_bot.send_message(message.chat.id, f"👥 Анкета Стажировки\n\n"
                                                        f"🏢 Название компании: {bd_job[self.count][1]}\n"
                                                        f"💼 Должность стажера: {bd_job[self.count][3]}\n"
                                                        f"📋 Требования к стажеру: {bd_job[self.count][4]}\n"
                                                        f"🌟 Условия стажировки: {bd_job[self.count][6]}\n"
                                                        f"⏰ Обязанности: {bd_job[self.count][4]}\n"
                                                        f"💰 Зарплата (если предусмотрено): {bd_job[self.count][7]}")
                job_bot.register_next_step_handler(msg, self.feed)

            elif message.text == "❤":
                print(f"{self.data[1]} лайкнул {bd_job[self.count_pred][1]}")

                if bd_job[self.count_pred][0] in vacancy_resume:
                    if f'@{message.from_user.username}' in [i["username"] for i in
                                                            vacancy_resume[bd_job[self.count_pred][0]]]:
                        job_bot.send_message(message.chat.id, "Вы уже лайкнули этого работадателя\nВидно он еще не ответил!")

                    else:
                        vacancy_resume[bd_job[self.count_pred][0]].append({"username": f'@{message.from_user.username}', "text": f'@{self.data[1]}\n'
                                                                                                                f'Имя: {self.data[2]}\n'
                                                                                                                f'Описание себя: {self.data[4]}\n'
                                                                                                                f'Лайкнул анкету\n'
                                                                                                                f"👥 Анкета Стажировки\n\n"
                                                                                                                f"🏢 Название компании: {bd_job[self.count_pred][1]}\n"
                                                                                                                f"💼 Должность стажера: {bd_job[self.count_pred][3]}\n"
                                                                                                                f"📋 Требования к стажеру: {bd_job[self.count_pred][4]}\n"
                                                                                                                f"🌟 Условия стажировки: {bd_job[self.count_pred][6]}\n"
                                                                                                                f"⏰ Обязанности: {bd_job[self.count_pred][4]}\n"
                                                                                                                f"💰 Зарплата (если предусмотрено): {bd_job[self.count_pred][7]}"})
                        job_bot.send_message(random.choice(admin_list),
                                             f'@{self.data[1]}\n'
                                             f'Имя: {self.data[2]}\n'
                                             f'Описание себя: {self.data[4]}\n'
                                             f'Лайкнул анкету\n'
                                             f"👥 Анкета Стажировки\n\n"
                                             f"🏢 Название компании: {bd_job[self.count_pred][1]}\n"
                                             f"💼 Должность стажера: {bd_job[self.count_pred][3]}\n"
                                             f"📋 Требования к стажеру: {bd_job[self.count_pred][4]}\n"
                                             f"🌟 Условия стажировки: {bd_job[self.count_pred][6]}\n"
                                             f"⏰ Обязанности: {bd_job[self.count_pred][4]}\n"
                                             f"💰 Зарплата (если предусмотрено): {bd_job[self.count_pred][7]}", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Подошел, удалить!", callback_data="like")).add(types.InlineKeyboardButton("Не подошел", callback_data="dislike")))
                else:
                    vacancy_resume[bd_job[self.count_pred][0]] = [{"username": f'@{message.from_user.username}', "text": f'@{self.data[1]}\n'
                                                                                                                f'Имя: {self.data[2]}\n'
                                                                                                                f'Описание себя: {self.data[4]}\n'
                                                                                                                f'Лайкнул анкету\n'
                                                                                                                f"👥 Анкета Стажировки\n\n"
                                                                                                                f"🏢 Название компании: {bd_job[self.count_pred][1]}\n"
                                                                                                                f"💼 Должность стажера: {bd_job[self.count_pred][3]}\n"
                                                                                                                f"📋 Требования к стажеру: {bd_job[self.count_pred][4]}\n"
                                                                                                                f"🌟 Условия стажировки: {bd_job[self.count_pred][6]}\n"
                                                                                                                f"⏰ Обязанности: {bd_job[self.count_pred][4]}\n"
                                                                                                                f"💰 Зарплата (если предусмотрено): {bd_job[self.count_pred][7]}"}]
                    job_bot.send_message(random.choice(admin_list),
                                         f'@{self.data[1]}\n'
                                         f'Имя: {self.data[2]}\n'
                                         f'Описание себя: {self.data[4]}\n'
                                         f'Лайкнул анкету\n'
                                         f"👥 Анкета Стажировки\n\n"
                                         f"🏢 Название компании: {bd_job[self.count_pred][1]}\n"
                                         f"💼 Должность стажера: {bd_job[self.count_pred][3]}\n"
                                         f"📋 Требования к стажеру: {bd_job[self.count_pred][4]}\n"
                                         f"🌟 Условия стажировки: {bd_job[self.count_pred][6]}\n"
                                         f"⏰ Обязанности: {bd_job[self.count_pred][4]}\n"
                                         f"💰 Зарплата (если предусмотрено): {bd_job[self.count_pred][7]}", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Подошел, удалить!", callback_data="like")).add(types.InlineKeyboardButton("Не подошел", callback_data="dislike")))
                print(vacancy_resume)
                msg = job_bot.send_message(message.chat.id, f"👥 Анкета Стажировки\n\n"
                                                        f"🏢 Название компании: {bd_job[self.count][1]}\n"
                                                        f"💼 Должность стажера: {bd_job[self.count][3]}\n"
                                                        f"📋 Требования к стажеру: {bd_job[self.count][4]}\n"
                                                        f"🌟 Условия стажировки: {bd_job[self.count][6]}\n"
                                                        f"⏰ Обязанности: {bd_job[self.count][4]}\n"
                                                        f"💰 Зарплата (если предусмотрено): {bd_job[self.count][7]}")
                job_bot.register_next_step_handler(msg, self.feed)

            elif message.text == "💤":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
                btn2 = types.KeyboardButton("👥 Моя анкета")
                btn4 = types.KeyboardButton("📞 Контакты")
                btn5 = types.KeyboardButton("📞 Оставить отзыв")

                markup.row(btn1, btn2).row(btn4, btn5)

                job_bot.send_message(message.chat.id, 'Добро пожаловать в бота "Стажировки для студентов"! 🚀🎓\n'
                                                  'Здесь ты найдешь удобный и быстрый способ находить интересные и перспективные стажировки. Мы поможем тебе стартовать в карьере, предоставив доступ к разнообразным предложениям от ведущих компаний.\n'
                                                  'Чтобы начать, выбери одну из опций в меню или введи ключевое слово, связанное с интересующей тебя областью. Мы постараемся сделать поиск стажировок максимально удобным и эффективным!\n'
                                                  'Если у тебя есть вопросы или нужна помощь, не стесняйся обращаться. Удачи в поиске стажировки! 💼🌐',
                                 reply_markup=markup)

    def feed_after(self, message):
        bd_job = feed_job(self.data[3])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("❤")
        btn2 = types.KeyboardButton("👎")
        btn3 = types.KeyboardButton("💤")

        markup.row(btn1, btn2, btn3)

        msg = job_bot.send_message(message.chat.id, f"👥 Анкета Стажировки\n\n"
                                                f"🏢 Название компании: {bd_job[self.count][1]}\n"
                                                f"💼 Должность стажера: {bd_job[self.count][3]}\n"
                                                f"📋 Требования к стажеру: {bd_job[self.count][4]}\n"
                                                f"🌟 Условия стажировки: {bd_job[self.count][6]}\n"
                                                f"⏰ Обязанности: {bd_job[self.count][4]}\n"
                                                f"💰 Зарплата (если предусмотрено): {bd_job[self.count][7]}")
        job_bot.register_next_step_handler(msg, self.feed)


class SkillsFeed:
    def __init__(self, count, data):
        self.count = count
        self.data = data
        self.ads_count = 0

    def feed(self, message):
        bd_skills = feed_skills(self.data[0], self.data[3], self.data[5], self.data[8])
        flag = True
        is_count = True

        if message.chat.id in skills_users:
            if len(skills_users[message.chat.id]) > 0:
                markup = types.InlineKeyboardMarkup()

                btn1 = types.InlineKeyboardButton("Лайк", callback_data="like")
                btn2 = types.InlineKeyboardButton("Дизлайк", callback_data="dislike")

                markup.add(btn1)
                markup.add(btn2)

                for i in range(len(skills_users[message.chat.id])):
                    skills_bot.send_message(message.chat.id, text=skills_users[message.chat.id][i]["text"], reply_markup=markup)
                msg = skills_bot.send_message(message.chat.id, "Ответьте на сообщения!", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Окей")))
                skills_bot.register_next_step_handler(msg, self.feed)
                return

        if message.text == "Окей":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("❤")
            btn2 = types.KeyboardButton("👎")
            btn3 = types.KeyboardButton("💤")

            markup.row(btn1, btn2, btn3)

            msg = skills_bot.send_message(message.chat.id, f"👥 Анкета Обмена Навыками\n\n"
                                                    f"👤 Меня зовут: {bd_skills[self.count][1]}\n"
                                                    f"🏡 Ищу человека в: {bd_skills[self.count][3]}\n"
                                                    f"📅 Мой возраст: {bd_skills[self.count][4]}\n"
                                                    f"🔍 Обо мне: {bd_skills[self.count][6]}\n"
                                                    f"🔍 О тебе: {bd_skills[self.count][7]}", reply_markup=markup)
            skills_bot.register_next_step_handler(msg, self.feed)
            return

        self.ads_count += 1

        if self.ads_count > 30:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn = types.KeyboardButton("Окей")
            markup.add(btn)

            msg = skills_bot.send_message(message.chat.id, "Пожалуйста, подпишитесь на наш основной канал: "
                                                    "<a href='https://t.me/+S46mvD24xeFhZWIy'>Студлайф</a>\n"
                                                    "В нем много интересной информации и другие полезные микросервисы для вас\n\n"
                                                    "С уважением команда Studlife", parse_mode="HTML",
                                   reply_markup=markup)
            skills_bot.register_next_step_handler(msg, self.feed_after)
            self.ads_count = 0
            return

        self.count_pred = self.count

        for i in range(self.count + 1, len(bd_skills)):
            if bd_skills[i][9] == 1:
                self.count = i
                print(self.count)
                flag = False
                is_count = False
                break

        if flag:
            for i in range(len(bd_skills)):
                if bd_skills[i][9] == 1:
                    is_count = False
                    self.count_pred = self.count
                    self.count = i
                    break

        if is_count or len(bd_skills) == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn3 = types.KeyboardButton("❌ Удалить анкету")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2, btn3).row(btn4, btn5)

            skills_bot.send_message(message.chat.id, "Анкет нет!", reply_markup=markup)

        else:
            if message.text == "👎":
                msg = skills_bot.send_message(message.chat.id, f"👥 Анкета Обмена Навыками\n\n"
                                                        f"👤 Меня зовут: {bd_skills[self.count][1]}\n"
                                                        f"🏡 Ищу соседа в: {bd_skills[self.count][3]}\n"
                                                        f"📅 Мой возраст: {bd_skills[self.count][4]}\n"
                                                        f"🔍 Обо мне: {bd_skills[self.count][6]}\n"
                                                        f"🔍 О тебе: {bd_skills[self.count][7]}")
                skills_bot.register_next_step_handler(msg, self.feed)

            elif message.text == "❤":
                print(f"{self.data[1]} лайкнул {bd_skills[self.count_pred][1]}")

                if bd_skills[self.count_pred][0] in skills_users:
                    if f'@{message.from_user.username}' in [i["username"] for i in
                                                            skills_users[bd_skills[self.count_pred][0]]]:
                        skills_bot.send_message(message.chat.id, "Вы уже лайкнули этого пользователя!\nВидно он еще не ответил!")

                    else:
                        skills_users[bd_skills[self.count - 1][0]].append({"username": f'@{message.from_user.username}',
                                                                  "text": f"{self.data[1]} лайнкул/а вашу анкету\n\n"
                                                                          f"👤 Меня зовут: {self.data[1]}\n"
                                                                          f"🏡 Ищу человека в: {self.data[3]}\n"
                                                                          f"📅 Мой возраст: {self.data[4]}\n"
                                                                          f"🔍 Обо мне: {self.data[6]}\n"
                                                                          f"🔍 О тебе: {self.data[7]}"})
                else:
                    skills_users[bd_skills[self.count_pred][0]] = [{"username": f'@{message.from_user.username}',
                                                           "text": f"{self.data[1]} лайнкул/а вашу анкету\n\n"
                                                                   f"👤 Меня зовут: {self.data[1]}\n"
                                                                   f"🏡 Ищу человека в: {self.data[3]}\n"
                                                                   f"📅 Мой возраст: {self.data[4]}\n"
                                                                   f"🔍 Обо мне: {self.data[6]}\n"
                                                                   f"🔍 О тебе: {self.data[7]}"}]
                msg = skills_bot.send_message(message.chat.id, f"👥 Анкета Обмена Навыками\n\n"
                                                        f"👤 Меня зовут: {bd_skills[self.count][1]}\n"
                                                        f"🏡 Ищу человека в: {bd_skills[self.count][3]}\n"
                                                        f"📅 Мой возраст: {bd_skills[self.count][4]}\n"
                                                        f"🔍 Обо мне: {bd_skills[self.count][6]}\n"
                                                        f"🔍 О тебе: {bd_skills[self.count][7]}")

                skills_bot.register_next_step_handler(msg, self.feed)

            elif message.text == "💤":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
                btn2 = types.KeyboardButton("👥 Моя анкета")
                btn3 = types.KeyboardButton("❌ Удалить анкету")
                btn4 = types.KeyboardButton("📞 Контакты")
                btn5 = types.KeyboardButton("📞 Оставить отзыв")

                markup.row(btn1, btn2, btn3).row(btn4, btn5)

                skills_bot.send_message(message.chat.id, 'Добро пожаловать в бот "Обмен навыками"! 🔄🤝\n'
                                             'Здесь ты сможешь найти партнеров для обмена навыками и знаний. Обучение становится увлекательным, когда есть кто-то, с кем можно делиться опытом и учиться новому!\n'
                                             'Выбери раздел в меню или введи ключевое слово, чтобы начать. Мы постараемся подобрать для тебя идеальных партнеров, с которыми обучение станет интересным и продуктивным!\n'
                                             'Если у тебя возникнут вопросы или нужна помощь, не стесняйся обращаться. Удачи в обмене навыками! 🚀📚🔁',
                                 reply_markup=markup)

    def feed_after(self, message):
        bd_skills = feed_skills(self.data[0], self.data[3], self.data[5], self.data[8])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("❤")
        btn2 = types.KeyboardButton("👎")
        btn3 = types.KeyboardButton("💤")

        markup.row(btn1, btn2, btn3)

        msg = skills_bot.send_message(message.chat.id, f"👥 Анкета Обмена Навыками\n\n"
                                                f"👤 Меня зовут: {bd_skills[self.count][1]}\n"
                                                f"🏡 Ищу соседа в: {bd_skills[self.count][3]}\n"
                                                f"📅 Мой возраст: {bd_skills[self.count][4]}\n"
                                                f"🔍 Обо мне: {bd_skills[self.count][6]}\n"
                                                f"🔍 О тебе: {bd_skills[self.count][7]}", reply_markup=markup)
        skills_bot.register_next_step_handler(msg, self.feed)
