import telebot
import language_tool_python
TOKEN = "8719496821:AAESVxDG92tL96BZVUys65p9JfUnwCMw_W4"
bot = telebot.TeleBot(TOKEN)
tool = language_tool_python.LanguageTool('ru-RU') 

# /start - команда для запуска бота
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот, который умеет решать примеры и проверять текст на ошибки.\n\n"
        "Напиши /help, чтобы узнать команды."
    )

# /help - команда для помощи
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n\n"
        "/start - запустить бота\n"
        "/help - список команд\n"
        "/text - проверить текст на ошибки\n"
        "/primer - решить математический пример"
    )
    
# /text - команда для проверки текста
@bot.message_handler(commands=['text'])
def text_command(message):
    bot.send_message(
        message.chat.id,
        "Отправь текст, который нужно проверить."
    )
    bot.register_next_step_handler(message, check_text)

# Проверка текста
def check_text(message):
    original_text = message.text
    matches = tool.check(original_text)
    if not matches:
        bot.reply_to(
            message,
            "Ошибок не найдено, текст написан правильно."
        )
        return
    corrected_text = tool.correct(original_text)
    response = (
        f"Исходный текст:\n"
        f"{original_text}\n\n"
        f"Исправленный текст:\n"
        f"{corrected_text}\n\n"
        f"Найдено ошибок: {len(matches)}"
    )
    bot.reply_to(message, response)

# /primer - кмд для реш. примеров
@bot.message_handler(commands=['primer'])
def example_command(message):
    bot.send_message(
        message.chat.id,
        "Отправь математический пример.\n\n"
        "Например:\n"
        "25 + 15 * 2"
    )
    bot.register_next_step_handler(message, solve_example)

# Решение примера
def solve_example(message):
    example = message.text
    allowed_chars = "0123456789+-*/.()% "
    if not all(c in allowed_chars for c in example):
        bot.reply_to(
            message,
            "❌Ошибка! Используй только цифры и математические операторы."
        )
        return
    try:
        result = eval(example)
        bot.reply_to(
            message,
            f"Пример: {example}\n"
            f"Результат: {result}"
        )
    except:
        bot.reply_to(
            message,
            "Не удалось решить пример😭. Проверь его правильность."
        )
print("Бот запущен...")
bot.polling(none_stop=True)