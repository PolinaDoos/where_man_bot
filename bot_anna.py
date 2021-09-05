from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import settings_anna
import logging

logging.basicConfig(filename='bot_anna.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# обход блокировой ТГ через прокси
PROXY = {'proxy_url': settings_anna.PROXY_URL,
        'urllib3_proxy_kwargs': {'username': settings_anna.PROXY_USERNAME, 'password': settings_anna.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Ну что ж, начнем')
    logging.info(f"{update.message.from_user['username']}, {update.message.from_user['first_name']} is trying to find out")
    update.message.reply_text(f"{update.message.from_user['first_name']}, Хочешь узнать, где твой мужик прямо сейчас? " + '\ud83d\ude0e')
    update.message.reply_text(f'Как зовут мужика, которого хочешь найти?')
    

def talk_to_me(update, context):
    user_text = update.message.text
    markup = ReplyKeyboardMarkup([['/Yes'], ['/No']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(f'{user_text} сейчас с тобой в одной комнате?', reply_markup = markup)
    

def yes(update, context):
    update.message.reply_text(f'Все в порядке, он не с другими телками')
    finish(update, context)    


def no(update, context):
    update.message.reply_text(f'Все в порядке, он не с другими телками даже за пределами комнаты')
    finish(update, context)


def finish(update, context):
    markup = ReplyKeyboardMarkup([['/start']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Хочешь проверить кого-то еще? Жми /start', reply_markup = markup)


def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings_anna.API_KEY, 
                    use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user)) # обработчик для команды start вызывает функцию greet_user
    dp.add_handler(CommandHandler("Yes", yes))
    dp.add_handler(CommandHandler("No", no))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # обработчик текста фильтрутет только текстовые сообщ
                                                             # и вызывает функцию talk_to_me
   
    logging.info('Bot just started')
    mybot.start_polling() # частые обращения за обновленияем

    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

if __name__ == "__main__":
    main()