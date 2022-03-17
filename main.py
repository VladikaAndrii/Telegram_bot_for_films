import telebot
import parsing_sites
from telebot import types
from db_queries import add_value_to_db, read_films_from_db
from settings import telegram_token

bot = telebot.TeleBot(telegram_token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """This feature creates interactive buttons for your Telegram bot"""
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Hello! I am at your service. ")
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        key_top_100_random = types.InlineKeyboardButton(text='Random movie from the TOP 250.',
                                                        callback_data='top_250')

        key_random_my_film = types.InlineKeyboardButton(text='Random movie from my list.',
                                                        callback_data='random_my_film')

        key_random_serial = types.InlineKeyboardButton(text='Random serial from the TOP 100.',
                                                       callback_data='random_serial_top_100')

        key_my_random_serial = types.InlineKeyboardButton(text='Random serial from my list.',
                                                          callback_data='random_my_serial')

        key_random_anime = types.InlineKeyboardButton(text='Random anime from the TOP 100.',
                                                      callback_data='random_anime_top_100')

        key_my_random_anime = types.InlineKeyboardButton(text='Random anime from my list.',
                                                         callback_data='random_my_anime')

        key_remember_film_for_me = types.InlineKeyboardButton(text='Save movie',
                                                              callback_data='remember_film_for_me')

        key_remember_serial_for_me = types.InlineKeyboardButton(text='Save the serial',
                                                                callback_data='remember_serial_for_me')

        key_remember_anime_for_me = types.InlineKeyboardButton(text='Save the anime',
                                                               callback_data='remember_anime_for_me')
        keyboard.add(key_top_100_random, key_random_my_film, key_random_serial, key_my_random_serial, key_random_anime,
                     key_my_random_anime, key_remember_film_for_me, key_remember_serial_for_me,
                     key_remember_anime_for_me)

        bot.send_message(message.from_user.id, text='What do I have to do?', reply_markup=keyboard)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Write - /start")

    else:
        bot.send_message(message.from_user.id, "My - yours not understand, write - /help, or /start.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """This function associates the button with its corresponding action"""

    if call.data == "top_250":
        bot.send_message(call.message.chat.id, "Second, I'm looking for information!")
        bot.send_message(call.message.chat.id, parsing_sites.ParseImdbSite().main())
    elif call.data == "random_my_film":
        content = 'movies'
        bot.send_message(call.message.chat.id, read_films_from_db(content))
    elif call.data == "random_serial_top_100":
        bot.send_message(call.message.chat.id, "Second, I'm looking for information!")
        bot.send_message(call.message.chat.id, parsing_sites.ParsingTopReyting().main())
    elif call.data == "random_my_serial":
        content = 'serials'
        bot.send_message(call.message.chat.id, read_films_from_db(content))
    elif call.data == 'random_anime_top_100':
        bot.send_message(call.message.chat.id, "Second, I'm looking for information!")
        bot.send_message(call.message.chat.id, parsing_sites.ParsingAnimego().main())
    elif call.data == 'random_my_anime':
        content = 'anime'
        bot.send_message(call.message.chat.id, read_films_from_db(content))
    elif call.data == 'remember_film_for_me':
        message_before_execution = bot.send_message(call.message.chat.id, 'What movie do you want to save?')

        def save_user_film(message):
            user_info = message.text
            name_of_table = 'movies'
            add_value_to_db(user_info, name_of_table)
            bot.send_message(call.message.chat.id, 'Successfully saved!')

        bot.register_next_step_handler(message_before_execution, save_user_film)

    elif call.data == 'remember_serial_for_me':
        message_before_execution = bot.send_message(call.message.chat.id, 'What serial do you want to save?')

        def save_user_serial(message):
            user_info = message.text
            name_of_table = 'serials'
            add_value_to_db(user_info, name_of_table)
            bot.send_message(call.message.chat.id, 'Successfully saved!')

        bot.register_next_step_handler(message_before_execution, save_user_serial)

    elif call.data == 'remember_anime_for_me':
        message_before_execution = bot.send_message(call.message.chat.id, 'What anime do you want to save?')

        def save_user_anime(message):
            user_info = message.text
            name_of_table = 'anime'
            add_value_to_db(user_info, name_of_table)
            bot.send_message(call.message.chat.id, 'Successfully saved!')

        bot.register_next_step_handler(message_before_execution, save_user_anime)

    else:
        for_other_values = "Unfortunately, I can't do more."
        bot.send_message(call.message.chat.id, for_other_values)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
