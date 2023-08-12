import functools
import threading

import telebot
from decouple import config
from telebot import types

bot = telebot.TeleBot(config("TOKEN")) #


def factorial_partial(start, end):
    """Считает факториал и возвращает результат"""
    result = 1
    for i in range(start, end + 1):
        result *= i
    return result


def threaded_factorial(n):
    """Принимает число, возвращает результат вычисления факториала используя потоки"""
    num_threads = 2  # используемое кол-во потоков
    chunk_size = n // num_threads

    thread_results = []

    def calculate_partial(start, end):
        partial_result = factorial_partial(start, end)
        thread_results.append(partial_result)

    threads = []
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i < num_threads - 1 else n
        thread = threading.Thread(target=calculate_partial, args=(start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_result = functools.reduce(lambda x, y: x * y, thread_results)
    return total_result


@bot.message_handler(commands=["start"])
def start(message):
    """Стартовое сообщение и кнопки, которые появляются при получении команды /start"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Посчитать факториал")
    btn2 = types.KeyboardButton("О боте")
    markup.add(btn1, btn2)
    bot.send_message(
        message.from_user.id,
        "Добро пожаловать. Я бот считающий факториал.",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "О боте")
def about_bot(message):
    """Сообщение отправляющееся при нажатии кнопки (О боте)"""
    remove_buttons = types.ReplyKeyboardRemove()
    bot.send_message(
        message.from_user.id,
        f"Наш бот помогает вычислить факториал числа.\nДля запуска бота введите /start.\nВыберите 'Посчитать факториал' и введите число. Бот вернет результат вычислений.\nДля завершения вычислений введите /exit",
        reply_markup=remove_buttons,
    )


@bot.message_handler(func=lambda message: message.text == "Посчитать факториал")
def get_text_messages(message):
    """Сообщение отправляющееся при нажатии кнопки Посчитать факториал"""
    if message.text == "Посчитать факториал":
        remove_buttons = types.ReplyKeyboardRemove()
        bot.send_message(
            message.from_user.id,
            "Введите число и я отправлю вам результат расчетов.",
            reply_markup=remove_buttons,
        )


@bot.message_handler(commands=["exit"])
def exit(message):
    """Выход из бота при получении команды /exit"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = types.KeyboardButton("/start")
    markup.add(btn_start)
    bot.send_message(
        message.from_user.id,
        f"Досвидания! Нажмите '/start' для начала работы с ботом.",
        reply_markup=markup,
    )


@bot.message_handler(
    func=lambda message: message.text.isdigit()
                         or (message.text.startswith("-") and message.text[1:].isdigit())
)
def calculate_factorial(message):
    """Принимает число. Возвращает результат расчета факториала."""
    num = int(message.text)
    if num >= 0:
        if num > 1000 or num < -1000:
            result = threaded_factorial(abs(num))
            result_str = str(result)
            bot.send_message(
                message.from_user.id,
                f"Результат подсчета - первые 5 чисел ответа: {result_str[:5]}",
            )
        else:
            result = threaded_factorial(abs(num))
            bot.send_message(message.from_user.id, f"Результат: {num}! = {result}")
    else:
        bot.send_message(
            message.from_user.id,
            f"Факториала отрицательного числа не существует. Введите положительное число",
        )


@bot.message_handler(func=lambda message: not message.text.isdigit())
def handle_invalid_number(message):
    """Обработка ошибки при выводе не числа"""
    bot.send_message(
        message.from_user.id, f"Я не могу расчитать факториал. Введите число!"
    )


bot.polling(none_stop=True, interval=0)
