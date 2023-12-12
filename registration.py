from telebot import types
from bd import *
from configs.config_mate import *
from configs.config_job import *
from configs.config_skills import *


class MateRegistration:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.username = data[2]
        self.address = data[3]
        self.age = data[4]
        self.price = data[5]
        self.sex_mate = data[6]
        self.desc_yourself = data[7]
        self.desc_you = data[8]
        self.sex = data[9]

    def get_fio(self, message):
        self.id = message.from_user.id
        self.username = message.from_user.username
        self.name = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("Мужской")
        btn2 = types.KeyboardButton("Женский")

        markup.row(btn1, btn2)

        msg = mate_bot.send_message(message.chat.id, "Твой пол:", reply_markup=markup)
        mate_bot.register_next_step_handler(msg, self.get_sex)

    def get_sex(self, message):
        self.sex = message.text
        if self.age:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text=self.age)
            markup.add(btn1)
            msg = mate_bot.send_message(message.chat.id, "Твой возраст:", reply_markup=markup)
        else:
            msg = mate_bot.send_message(message.chat.id, "Твой возраст:", reply_markup=types.ReplyKeyboardRemove())
        mate_bot.register_next_step_handler(msg, self.get_age)

    def get_age(self, message):
        if message.text.isdigit():
            self.age = message.text
            if self.address:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton(text=self.address)
                markup.add(btn1)
                msg = mate_bot.send_message(message.chat.id, "Твой город, где ты ищешь соседа:",
                                       reply_markup=markup)
            else:
                msg = mate_bot.send_message(message.chat.id, "Твой город, где ты ищешь соседа:", reply_markup=types.ReplyKeyboardRemove())

            mate_bot.register_next_step_handler(msg, self.get_location)
        else:
            msg = mate_bot.send_message(message.chat.id, "Только цифры!")

            mate_bot.register_next_step_handler(msg, self.get_age)

    def get_location(self, message):
        loc = geolocator.geocode(message.text)

        if loc:

            address = geolocator.reverse((loc.latitude, loc.longitude)).raw["address"]

            town = address.get('town', '')
            city = address.get('city', '')
            state = address.get('state', '')

            if town != "":
                self.address = town
            elif city != "":
                self.address = city
            else:
                self.address = state

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("✔ Все верно")
            btn2 = types.KeyboardButton("❌ Нет, переписать")

            markup.row(btn1, btn2)

            msg = mate_bot.send_message(message.chat.id, f'{loc}\nВерный адрес?', reply_markup=markup)

            mate_bot.register_next_step_handler(msg, self.choice)

        else:
            msg = mate_bot.send_message(message.chat.id, "Неверный адрес\nПожалуйста, попробуйте снова:")
            mate_bot.register_next_step_handler(msg, self.get_location)

    def choice(self, message):
        if message.text == "✔ Все верно":
            if self.price:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton(text=self.price)
                markup.add(btn1)
                msg = mate_bot.send_message(message.chat.id, "Твой бюджет (Например: 25000 рублей):", reply_markup=markup)
            else:
                msg = mate_bot.send_message(message.chat.id, "Твой бюджет (Например: 25000 рублей):", reply_markup=types.ReplyKeyboardRemove())
            mate_bot.register_next_step_handler(msg, self.get_price)


        elif message.text == "❌ Нет, переписать":
            msg = mate_bot.send_message(message.chat.id, "Твой город, где ты ищешь соседа:", reply_markup=types.ReplyKeyboardRemove())
            mate_bot.register_next_step_handler(msg, self.get_location)


    def get_price(self, message):
        self.price = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("Парня")
        btn2 = types.KeyboardButton("Девушку")

        markup.row(btn1, btn2)

        msg = mate_bot.send_message(message.chat.id,
                               "Кого ты ищешь: ", reply_markup=markup)
        mate_bot.register_next_step_handler(msg, self.get_sex_mate)

    def get_sex_mate(self, message):
        if message.text == "Парня":
            self.sex_mate = "Мужской"
        elif message.text == "Девушку":
            self.sex_mate = "Женский"
        else:
            msg = mate_bot.send_message(message.chat.id,
                                   "Нет такого ответа, попробуйте снова")
            mate_bot.register_next_step_handler(msg, self.get_sex_mate)

        if self.desc_yourself:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("Оставить текущее")

            markup.add(btn1)

            msg = mate_bot.send_message(message.chat.id,
                                   "Опиши, каким соседом и человеком ты себя считаешь\n(Дайте больше информации о себе):", reply_markup=markup)
        else:
            msg = mate_bot.send_message(message.chat.id,
                                   "Опиши, каким соседом и человеком ты себя считаешь\n(Дайте больше информации о себе):",
                                   reply_markup=types.ReplyKeyboardRemove())
        mate_bot.register_next_step_handler(msg, self.get_desc_yourself)

    def get_desc_yourself(self,message):
        if message.text != "Оставить текущее":
            self.desc_yourself = message.text

        if self.desc_you:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("Оставить текущее")

            markup.add(btn1)

            msg = mate_bot.send_message(message.chat.id,
                                   "Требования к соседу\nКаким он должен быть в твоем понимании:", reply_markup=markup)
        else:

            msg = mate_bot.send_message(message.chat.id,
                                   "Требования к соседу\nКаким он должен быть в твоем понимании:", reply_markup=types.ReplyKeyboardRemove())
        mate_bot.register_next_step_handler(msg, self.get_desc_you)


    def get_desc_you(self, message):
        if message.text != "Оставить текущее":
            self.desc_you = message.text

        register_mate(self.id, self.name, self.username, self.address, self.age, self.price, self.sex_mate, self.desc_yourself, self.desc_you, self.sex)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
        btn2 = types.KeyboardButton("👥 Моя анкета")
        btn3 = types.KeyboardButton("❌ Удалить анкету")
        btn4 = types.KeyboardButton("📞 Контакты")
        btn5 = types.KeyboardButton("📞 Оставить отзыв")

        markup.row(btn1, btn2, btn3).row(btn4, btn5)

        mate_bot.send_message(message.chat.id, f"👥 Ваша Анкета Соседа\n"
                                          f"👤 Меня зовут: {self.name}\n"
                                          f"🏡 Ищу соседа в: {self.address}\n"
                                          f"📅 Мой возраст: {self.age}\n"
                                          f"💰 Бюджет: {self.price}\n"
                                          f"🔍 Обо мне: {self.desc_yourself}\n"
                                          f"🔍 О тебе: {self.desc_you}", reply_markup=markup)


class ResumeRegistration:
    def __init__(self, data):
        self.id = data[0]
        self.username = data[1]
        self.name = data[2]
        self.address = data[3]
        self.desc_yourself = data[4]

    def get_fio(self, message):
        self.id = message.from_user.id
        self.username = message.from_user.username
        self.name = message.text
        if self.address:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text=self.address)
            markup.add(btn1)
            msg = job_bot.send_message(message.chat.id, "Твой город, где ты ищешь стажировку:",
                                   reply_markup=markup)
        else:
            msg = job_bot.send_message(message.chat.id, "Твой город, где ты ищешь стажировку:",
                                   reply_markup=types.ReplyKeyboardRemove())

        job_bot.register_next_step_handler(msg, self.get_location)

    def get_location(self, message):
        loc = geolocator_job.geocode(message.text)

        if loc:

            address = geolocator_job.reverse((loc.latitude, loc.longitude)).raw["address"]

            town = address.get('town', '')
            city = address.get('city', '')
            state = address.get('state', '')

            if town != "":
                self.address = town
            elif city != "":
                self.address = city
            else:
                self.address = state

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("✔ Все верно")
            btn2 = types.KeyboardButton("❌ Нет, переписать")

            markup.row(btn1, btn2)

            msg = job_bot.send_message(message.chat.id, f'{loc}\nВерный адрес?', reply_markup=markup)

            job_bot.register_next_step_handler(msg, self.choice)

        else:
            msg = job_bot.send_message(message.chat.id, "Неверный адрес\nПожалуйста, попробуйте снова:")
            job_bot.register_next_step_handler(msg, self.get_location)

    def choice(self, message):
        if message.text == "✔ Все верно":
            if self.desc_yourself:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton(text=self.desc_yourself)
                markup.add(btn1)
                msg = job_bot.send_message(message.chat.id, "Опишите себя, свои качества и свои умения:", reply_markup=markup)
            else:
                msg = job_bot.send_message(message.chat.id, "Опишите себя, свои качества и свои умения:",
                                       reply_markup=types.ReplyKeyboardRemove())

            job_bot.register_next_step_handler(msg, self.get_desc_yourself)


        elif message.text == "❌ Нет, переписать":
            msg = job_bot.send_message(message.chat.id, "Твой город, где ты ищешь стажировку:",
                                   reply_markup=types.ReplyKeyboardRemove())
            job_bot.register_next_step_handler(msg, self.get_location)

    def get_desc_yourself(self, message):
        if message.text != "Оставить текущее":
            self.desc_yourself = message.text

        register_resume(self.id, self.name, self.username, self.address, self.desc_yourself)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
        btn2 = types.KeyboardButton("👥 Моя анкета")
        btn3 = types.KeyboardButton("❌ Удалить анкету")
        btn4 = types.KeyboardButton("📞 Контакты")
        btn5 = types.KeyboardButton("📞 Оставить отзыв")

        markup.row(btn1, btn2, btn3).row(btn4, btn5)

        job_bot.send_message(message.chat.id, 'Добро пожаловать в бота "Стажировки для студентов"! 🚀🎓\n'
                                              'Здесь ты найдешь удобный и быстрый способ находить интересные и перспективные стажировки. Мы поможем тебе стартовать в карьере, предоставив доступ к разнообразным предложениям от ведущих компаний.\n'
                                              'Чтобы начать, выбери одну из опций в меню или введи ключевое слово, связанное с интересующей тебя областью. Мы постараемся сделать поиск стажировок максимально удобным и эффективным!\n'
                                              'Если у тебя есть вопросы или нужна помощь, не стесняйся обращаться. Удачи в поиске стажировки! 💼🌐',
                             reply_markup=markup)


class VacancyRegistration:
    def __init__(self):
        self.name = None
        self.address = None
        self.post = None
        self.responsibilities = None
        self.requirements = None
        self.conditions = None
        self.salary = None

    def get_fio(self, message):
        self.name = message.text

        msg = job_bot.send_message(message.chat.id, "Город:")

        job_bot.register_next_step_handler(msg, self.get_location)

    def get_location(self, message):
        loc = geolocator_job.geocode(message.text)

        if loc:

            address = geolocator_job.reverse((loc.latitude, loc.longitude)).raw["address"]

            town = address.get('town', '')
            city = address.get('city', '')
            state = address.get('state', '')

            if town != "":
                self.address = town
            elif city != "":
                self.address = city
            else:
                self.address = state

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("✔ Все верно")
            btn2 = types.KeyboardButton("❌ Нет, переписать")

            markup.row(btn1, btn2)

            msg = job_bot.send_message(message.chat.id, f'{loc}\nВерный адрес?', reply_markup=markup)

            job_bot.register_next_step_handler(msg, self.choice)

        else:
            msg = job_bot.send_message(message.chat.id, "Неверный адрес\nПожалуйста, попробуйте снова:")
            job_bot.register_next_step_handler(msg, self.get_location)

    def choice(self, message):
        if message.text == "✔ Все верно":
            msg = job_bot.send_message(message.chat.id, "Должность:")

            job_bot.register_next_step_handler(msg, self.get_post)


        elif message.text == "❌ Нет, переписать":
            msg = job_bot.send_message(message.chat.id, "Город:")
            job_bot.register_next_step_handler(msg, self.get_location)

    def get_post(self, message):
        self.post = message.text

        msg = job_bot.send_message(message.chat.id, "Обязаности:")

        job_bot.register_next_step_handler(msg, self.get_responsibilities)

    def get_responsibilities(self, message):
        self.responsibilities = message.text

        msg = job_bot.send_message(message.chat.id, "Требования:")

        job_bot.register_next_step_handler(msg, self.get_requirements)

    def get_requirements(self, message):
        self.requirements = message.text

        msg = job_bot.send_message(message.chat.id, "Условия:")

        job_bot.register_next_step_handler(msg, self.get_conditions)

    def get_conditions(self, message):
        self.conditions = message.text

        msg = job_bot.send_message(message.chat.id, "Зарплата:")

        job_bot.register_next_step_handler(msg, self.get_salary)


    def get_salary(self, message):
        self.salary = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("✔ Все верно")
        btn2 = types.KeyboardButton("❌ Нет, переписать")

        markup.row(btn1, btn2)
        job_bot.send_message(message.chat.id, f"👥 Анкета Стажировки\n\n"
                                                        f"🏢 Название компании: {self.name}\n"
                                                        f"💼 Должность стажера: {self.post}\n"
                                                        f"📋 Требования к стажеру: {self.requirements}\n"
                                                        f"🌟 Условия стажировки: {self.conditions}\n"
                                                        f"⏰ Обязанности: {self.responsibilities}\n"
                                                        f"💰 Зарплата (если предусмотрено): {self.salary}")
        msg = job_bot.send_message(message.chat.id, "Все верно?:", reply_markup=markup)

        job_bot.register_next_step_handler(msg, self.get_end)

    def get_end(self, message):
        if message.text == "✔ Все верно":

            register_job(self.name, self.address, self.post, self.responsibilities, self.requirements, self.conditions, self.salary)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
            btn2 = types.KeyboardButton("👥 Моя анкета")
            btn4 = types.KeyboardButton("📞 Контакты")
            btn5 = types.KeyboardButton("📞 Оставить отзыв")

            markup.row(btn1, btn2).row(btn4, btn5)

            job_bot.send_message(message.chat.id, 'Анкета добавлена',
                                 reply_markup=markup)
        else:
            job_bot.send_message(message.chat.id, "Введите название компании:")
            job_bot.register_next_step_handler(message, self.get_fio)


class SkillsRegistration:
    def __init__(self, data):
        print(data)
        self.id = data[0]
        self.name = data[1]
        self.username = data[2]
        self.address = data[3]
        self.age = data[4]
        self.sex_skills = data[5]
        self.desc_yourself = data[6]
        self.desc_you = data[7]
        self.sex = data[8]

    def get_fio(self, message):
        self.id = message.from_user.id
        self.username = message.from_user.username
        self.name = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("Мужской")
        btn2 = types.KeyboardButton("Женский")

        markup.row(btn1, btn2)

        msg = skills_bot.send_message(message.chat.id, "Твой пол:", reply_markup=markup)
        skills_bot.register_next_step_handler(msg, self.get_sex)

    def get_sex(self, message):
        self.sex = message.text
        if self.age:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text=self.age)
            markup.add(btn1)
            msg = skills_bot.send_message(message.chat.id, "Твой возраст:", reply_markup=markup)
        else:
            msg = skills_bot.send_message(message.chat.id, "Твой возраст:", reply_markup=types.ReplyKeyboardRemove())
        skills_bot.register_next_step_handler(msg, self.get_age)

    def get_age(self, message):
        if message.text.isdigit():
            self.age = message.text
            if self.address:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton(text=self.address)
                markup.add(btn1)
                msg = skills_bot.send_message(message.chat.id, "Твой город:",
                                       reply_markup=markup)
            else:
                msg = skills_bot.send_message(message.chat.id, "Твой город:", reply_markup=types.ReplyKeyboardRemove())

            skills_bot.register_next_step_handler(msg, self.get_location)
        else:
            msg = skills_bot.send_message(message.chat.id, "Только цифры!")

            skills_bot.register_next_step_handler(msg, self.get_age)

    def get_location(self, message):
        loc = geolocator_skills.geocode(message.text)

        if loc:

            address = geolocator_skills.reverse((loc.latitude, loc.longitude)).raw["address"]

            town = address.get('town', '')
            city = address.get('city', '')
            state = address.get('state', '')

            if town != "":
                self.address = town
            elif city != "":
                self.address = city
            else:
                self.address = state

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("✔ Все верно")
            btn2 = types.KeyboardButton("❌ Нет, переписать")

            markup.row(btn1, btn2)

            msg = skills_bot.send_message(message.chat.id, f'{loc}\nВерный адрес?', reply_markup=markup)

            skills_bot.register_next_step_handler(msg, self.choice)

        else:
            msg = skills_bot.send_message(message.chat.id, "Неверный адрес\nПожалуйста, попробуйте снова:")
            skills_bot.register_next_step_handler(msg, self.get_location)

    def choice(self, message):
        if message.text == "✔ Все верно":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("Парня")
            btn2 = types.KeyboardButton("Девушку")

            markup.row(btn1, btn2)

            msg = skills_bot.send_message(message.chat.id,
                                        "Кого ты ищешь: ", reply_markup=markup)
            skills_bot.register_next_step_handler(msg, self.get_sex_skills)

        elif message.text == "❌ Нет, переписать":
            msg = skills_bot.send_message(message.chat.id, "Твой город:", reply_markup=types.ReplyKeyboardRemove())
            skills_bot.register_next_step_handler(msg, self.get_location)

    def get_sex_skills(self, message):
        if message.text == "Парня":
            self.sex_skills = "Мужской"
        elif message.text == "Девушку":
            self.sex_skills = "Женский"
        else:
            msg = skills_bot.send_message(message.chat.id,
                                   "Нет такого ответа, попробуйте снова")
            skills_bot.register_next_step_handler(msg, self.get_sex_skills)

        if self.desc_yourself:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("Оставить текущее")

            markup.add(btn1)

            msg = skills_bot.send_message(message.chat.id,
                                   "Опиши свои качества, умения и тд...:", reply_markup=markup)
        else:
            msg = skills_bot.send_message(message.chat.id,
                                   "Опиши свои качества, умения и тд...:",
                                   reply_markup=types.ReplyKeyboardRemove())
        skills_bot.register_next_step_handler(msg, self.get_desc_yourself)

    def get_desc_yourself(self,message):
        if message.text != "Оставить текущее":
            self.desc_yourself = message.text

        if self.desc_you:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn1 = types.KeyboardButton("Оставить текущее")

            markup.add(btn1)

            msg = skills_bot.send_message(message.chat.id,
                                   "Опиши качества, умения человека, которого ты ищешь:", reply_markup=markup)
        else:

            msg = skills_bot.send_message(message.chat.id,
                                   "Опиши качества, умения человека, которого ты ищешь:", reply_markup=types.ReplyKeyboardRemove())
        skills_bot.register_next_step_handler(msg, self.get_desc_you)


    def get_desc_you(self, message):
        if message.text != "Оставить текущее":
            self.desc_you = message.text

        register_skills(self.id, self.name, self.username, self.address, self.age, self.sex_skills, self.desc_yourself, self.desc_you, self.sex)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("🔍 Смотреть анкеты")
        btn2 = types.KeyboardButton("👥 Моя анкета")
        btn3 = types.KeyboardButton("❌ Удалить анкету")
        btn4 = types.KeyboardButton("📞 Контакты")
        btn5 = types.KeyboardButton("📞 Оставить отзыв")

        markup.row(btn1, btn2, btn3).row(btn4, btn5)

        skills_bot.send_message(message.chat.id, f"👥 Ваша Анкета Обмена Навыками\n"
                                          f"👤 Меня зовут: {self.name}\n"
                                          f"🏡 Ищу человека в: {self.address}\n"
                                          f"📅 Мой возраст: {self.age}\n"
                                          f"🔍 Обо мне: {self.desc_yourself}\n"
                                          f"🔍 О тебе: {self.desc_you}", reply_markup=markup)