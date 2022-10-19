from telegram.ext import *

print('Starting...')

# Lets us use the /start command
def start(update, context):
    update.message.reply_text('Witam')

# Lets us use the /help command
def help(update, context):
    update.message.reply_text('Dostępne komendy')

def handle_response(text) -> str:
    # Create your own response logic
    if 'hello' in text:
        return 'Hey there!'

    if 'how are you' in text:
        return 'I\'m good!'

    return 'I don\'t understand'


def handle_message(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if '@driver33bot' in text:
            new_text = text.replace('@driver33bot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    # Reply normal if the message is in private
    update.message.reply_text(response)

# Run the program
if __name__ == '__main__':
    updater = Updater('5656552566:AAG7JWW_zp7jB29b9-xqY7o0MwlVmLTYH40', use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()

