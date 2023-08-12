# Бот для подсчета факториала.

Тестовое задание по разработке бота для подсчета факториала. Этот проект представляет собой Telegram-бота, разработанного с использованием
библиотеки Telebot на языке программирования Python. Бот предназначен для вычисления факториалов чисел и вывода результатов пользователям.

## О проекте

### Что делает бот:

- Позволяет пользователю рассчитывать факториал числа.
- Реализована многопоточная стратегия вычисления для оптимизации производительности.
- При вводе числа, если оно больше 1000 или меньше -1000, выводит первые 5 цифр результата.
- Обработка ошибок: если ввели не число.

### Как использовать:

1. Начните диалог с ботом командой `/start`
2. Выберите опцию "Посчитать факториал" с помощью кнопки.
3. Введите число, для которого хотите вычислить факториал.
4. Бот выдаст результат вычислений.
5. Для выхода из бота введите: `/exit`

## Запуск проекта

1. Установите необходимые зависимости с помощью команды: `pip install -r requirements.txt`
2. Создайте .env файл, в который запишите: TOKEN=`ваш токен` из telebot
3. Запустите бота с помощью запуска файла `bot.py` 

## Сборка Docker контейнера

1. Сборки Docker контейнера: `docker build -t bot_app .`
2. Запуск Docker контейнера: `docker docker run -d bot_app`

