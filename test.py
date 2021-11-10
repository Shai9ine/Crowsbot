from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
from telegram.ext import InlineQueryHandler
from telegram.ext.filters import Filters

from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InputTextMessageContent
from telegram import InlineQueryResultArticle
from telegram import ParseMode
from telegram import error

from telegram.chataction import ChatAction

import logging
from uuid import uuid4

base_url = "https://toplearn.com/courses?search="
token = "your token"
messages = {
    "msg_start": "سلام {} {} \n به ربات تاپلرن خوش آمدید.",
    "msg_sum": "مجموع اعداد به صورت زیر است: \n {}",
    "msg_main_handler": "منو اصلی:",
    "msg_select_language": "زبان موردنظر خو را انتخاب کنید:",
    "msg_contact": "ارتباط با ما: \n کانال تلگرامی: \n وبسایت",

    "btn_courses": "دوره های موجود در سایت",
    "btn_articles": "مقالات",
    "btn_help": "راهنمایی",
    "btn_contact_us": "تماس با ما",
    "btn_python": "پایتون",
    "btn_kotlin": "کاتلین",
    "btn_return": "بازگشت"
}
conversations = {}
FIRST, SECOND = range(2)
logging.basicConfig(filename="info.log", filemode="a", level=logging.INFO, format="%(asctime)s-%(filename)s-%(message)s")


def start_handler(update: Update, context: CallbackContext):
    # when a user start the bot.

    # import pdb; pdb.set_trace()
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text="<i>سلام</i>", parse_mode=ParseMode.HTML)
    main_menu_handler(update, context)
    logging.info("({} - {}) start the bot.".format(first_name, chat_id))


def sum_handler(update: Update, context: CallbackContext):
    # return summation of input numbers.

    # import pdb; pdb.set_trace()
    chat_id = update.message.chat_id
    numbers = context.args
    result = sum(int(i) for i in numbers)
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["msg_sum"].format(result))


def main_menu_handler(update: Update, context: CallbackContext):
    # import pdb; pdb.set_trace()
    buttons = [
        [messages["btn_articles"], messages["btn_courses"]],
        [messages["btn_contact_us"]],
        [messages["btn_help"]]
    ]
    update.message.reply_text(
        text=messages["msg_main_handler"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def languages_handler(update: Update, context: CallbackContext):
    buttons = [
        [messages["btn_python"], messages["btn_kotlin"]],
        [messages["btn_return"]]
    ]
    update.message.reply_text(
        text=messages["msg_select_language"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def python_handler(update: Update, context: CallbackContext):
    text = ""
    courses, time, costs = get_data("python")
    for i in range(len(costs)):
        text += courses[i] + time[i] + costs[i] + "\n \n"
    update.message.reply_text(text=text)


def contact_handler(update: Update, context: CallbackContext):
    update.message.reply_text(text=messages["msg_contact"])


def return_handler(update: Update, context: CallbackContext):

    main_menu_handler(update, context)


def send_music_handler(update: Update, context: CallbackContext):
    # import pdb; pdb.set_trace()
    chat_id = update.message.chat_id
    try:
        with open("./Mohsen Yeganeh - Ghalbe Yakhi.mp3", "rb") as music:
            context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_AUDIO)
            context.bot.sendAudio(chat_id, music, caption="آهنگ مورد علاقه من", duration=600, disable_notification=True)
    except error.NetworkError as e:
        update.message.reply_text(text="شبکه مشکل دارد.")


def send_photo_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    with open("./logo.png", "rb") as img:
        context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
        context.bot.sendPhoto(chat_id, img, caption="لوگوی تاپلرن")


def send_doc_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    with open("./CHEM 3301L-ORGANIC I PRE-LAB QUESTIONS (FALL 2008).pdf", "rb") as doc:
        context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)
        context.bot.sendDocument(chat_id, doc, caption="فایل")


def keyboard_handler(update: Update, context: CallbackContext):
    buttons = [
        [
            InlineKeyboardButton("صفحه اصلی تاپلرن", callback_data="main"),
            InlineKeyboardButton("دوره های پایتون", callback_data="python")
        ]
    ]
    update.message.reply_text(
        text="صفحه مورد نظر را انتخاب بکنید:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def end_keyboard_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if data == "main":
        text = "شما صفحه اصلی تاپلرن را انتخاب کردید."
    else:
        text = "شما دوره های پایتون را انتخاب کردید."
    context.bot.editMessageText(text=text, chat_id=chat_id, message_id=message_id)


def glass_handler(update: Update, context: CallbackContext):
    buttons = [
        [
            InlineKeyboardButton("برنامه نویس", callback_data="programmer"),
            InlineKeyboardButton("ورزشکار", callback_data="athlete")
        ]
    ]
    update.message.reply_text(
        text="رشته موردنظر خود را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return FIRST


def programmer_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    buttons = [
        [
            InlineKeyboardButton("پایتون", callback_data="python"),
            InlineKeyboardButton("کاتلین", callback_data="kotlin")
        ]
    ]
    context.bot.editMessageText(text="زبان موردنظر را انتخاب کنید:",
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(buttons))
    return SECOND


def athlete_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    buttons = [
        [
            InlineKeyboardButton("فوتباال", callback_data="football"),
            InlineKeyboardButton("گلف", callback_data="golf")
        ]
    ]
    context.bot.editMessageText(text="رشته موردنظر را انتخاب کنید:",
                                chat_id=chat_id, message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(buttons))
    return SECOND


def end_handler(update: Update, context: CallbackContext):
    global conversations
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    conversations[chat_id] = data
    context.bot.editMessageText(
        text="{} به عنوان رشته موردعلاقه شما انتخاب شد.".format(conversations[chat_id]),
        chat_id=chat_id,
        message_id=message_id
    )
    return ConversationHandler.END


def inline_query_handler(update: Update, context: CallbackContext):
    query = update.inline_query.query
    result = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Uppercase",
            input_message_content=InputTextMessageContent(query.upper())
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent("<i>{}</i>".format(query), parse_mode=ParseMode.HTML)
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent("<b>{}</b>".format(query), parse_mode=ParseMode.HTML)
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Poem",
            input_message_content=InputTextMessageContent("<pre>{}</pre>".format(query), parse_mode=ParseMode.HTML)
        )
    ]
    update.inline_query.answer(result)


def main():
    updater = Updater(token, use_context=True)
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("glass", glass_handler)],
        states={
            FIRST: [CallbackQueryHandler(programmer_handler, pattern="^programmer$"),
                    CallbackQueryHandler(athlete_handler, pattern="^athlete$")],
            SECOND: [CallbackQueryHandler(end_handler)]
        },
        fallbacks=[CommandHandler("glass", glass_handler)],
        allow_reentry=True
    )
    updater.dispatcher.add_handler(conversation_handler)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("sum", sum_handler, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("music", send_music_handler))
    updater.dispatcher.add_handler(CommandHandler("photo", send_photo_handler))
    updater.dispatcher.add_handler(CommandHandler("keyboard", keyboard_handler))

    updater.dispatcher.add_handler(CallbackQueryHandler(end_keyboard_handler))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_courses"]), languages_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_return"]), return_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_python"]), python_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_contact_us"]), contact_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_articles"]), send_doc_handler))

    updater.dispatcher.add_handler(InlineQueryHandler(inline_query_handler))

    updater.start_polling()

    updater.idle()


main()
