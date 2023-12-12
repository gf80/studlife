import telebot
from telebot import types


TOKEN = ""


bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    # Button for the bot to find neighbors for students
    btn_neighbors = types.InlineKeyboardButton('🏠 Поиск соседей', url='https://t.me/studelifebot')
    markup.add(btn_neighbors)

    # Button for the bot to find vacancies and internships for students
    btn_vacancies = types.InlineKeyboardButton('💼 Поиск вакансий и стажировок', url='https://t.me/studlifevacancybot')
    markup.add(btn_vacancies)

    # Button for the bot to find people for skill exchange for students
    btn_skills = types.InlineKeyboardButton('🔄 Обмен навыками', url='https://t.me/studlifeskillsbot')
    markup.add(btn_skills)

    bot.send_message(message.chat.id, 'Привет! Я бот для студентов. Выбери интересующий тебя раздел:',
                     reply_markup=markup)


if __name__ == "__main__":
    bot.polling(none_stop=True)
