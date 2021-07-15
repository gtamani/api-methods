from datetime import datetime
from telegram.ext import *
from dotenv import load_dotenv
import os

load_dotenv()
api = os.environ.get("API")

print("Bot started!")

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ["hello","hi","hola"]:
        return "Hey, Como andas?"
    
    if user_message in ["quién sos?","quien sos?"]:
        return "Soy el mejor bot del mundo"

    if user_message in ["que hora es?","qué hora es?","hora","time"]:
        return datetime.now().strftime("%d/%m/%y %H:%M:%S")

def start_command(update,context):
    update.message.reply_text("Hola perri")

def help_command(update,context):
    update.message.reply_text("Si necesitas ayuda jodete")

def handle_message(update,context):
    text = update.message.text.lower()
    response = sample_responses(text)
    update.message.reply_text(response)

def error(update,context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(api,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(MessageHandler(Filters.text,handle_message))
    dp.add_error_handler(error)

    updater.start_polling(5)
    updater.idle()

main()