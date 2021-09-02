from telegram.ext import Updater, CommandHandler
import os

TOKEN = '1945231918:AAGOT70yF4YHAERfdlNRYIuvWbMV37I9yr8'
PORT = int(os.environ.get('PORT', 5000))
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher


def start(update, context):
    update.message.reply_text('Hi!')


dp.add_handler(CommandHandler('start', start))
updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN)
updater.bot.setWebhook('https://fathomless-dawn-41999.herokuapp.com/' + TOKEN)

updater.idle()
