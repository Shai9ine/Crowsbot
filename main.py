from telegram.ext import Updater, CommandHandler
import os

TOKEN = '1945231918:AAGOT70yF4YHAERfdlNRYIuvWbMV37I9yr8'
PORT = int(os.environ.get('PORT', 5000))
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN)
updater.bot.setWebhook('https://fathomless-dawn-41999.herokuapp.com/' + TOKEN)

updater.idle()
