from telegram import \
    Update,\
    ChatAction
# ---------------------------------------------
from telegram.ext import \
    Updater, \
    CommandHandler, \
    CallbackContext
# ----------------------------------------------
import os

# ----------------------------------------------
TOKEN = '1945231918:AAGOT70yF4YHAERfdlNRYIuvWbMV37I9yr8'
PORT = int(os.environ.get('PORT', 5000))
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher
# -----------------------------------------------
msgs = {
    'start-msg': '''
    < درود {} عزیز >
به Crows BOT خوش آمدید.🍻
    '''
}


# -----------------------------------------------


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    full_name = update.message.chat.full_name
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(msgs['start-msg'].format(full_name))


# ----------------------------------------------

dp.add_handler(CommandHandler('start', start))
# -----------------------------------------------
updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN)
updater.bot.setWebhook('https://fathomless-dawn-41999.herokuapp.com/' + TOKEN)
updater.idle()
