from telegram.ext import *
from FlightRadar24.api import FlightRadar24API
print("Starting...")
#api
def getf():
    fr_api = FlightRadar24API()
    fl = ""
    #{'tl_y': 50.68, 'tl_x': 20.94, 'br_y': 49.55, 'br_x': 23.09}
    zone = {'tl_y': 50.68, 'tl_x': 20.94, 'br_y': 49.55, 'br_x': 23.09}
    bounds = fr_api.get_bounds(zone)
    flights = fr_api.get_flights(bounds = bounds)

    for f in flights:
        try:
            details = fr_api.get_flight_details(f.id)
            f.set_flight_details(details)
            if f.destination_airport_name == "Rzeszow Jasionka Airport":
                #print("From:",f.origin_airport_country_name, ",status:", f.status_text)
                fl += "From: " + f.origin_airport_country_name + " ,status: " + f.status_text + "\n"
            #print(f.time_details["estimated"]["arrival"])
            #date_time_obj = datetime.strptime(f.time_details["estimated"]["arrival"], '%d/%m/%y %H:%M:%S')
        except:
            pass
    return fl

#bot
def start(update, context):
    update.message.reply_text('Witam')

def help(update, context):
    update.message.reply_text('Dostępne komendy: start, help, auto, auto2, stop')

def callback_auto_message(context):
    try:
        context.bot.send_message(chat_id='-1001803015206', text=getf())
    except:
        pass
        #context.bot.send_message(chat_id='1603466015', text="Nie ma samolotow chlopie")

def start_auto_messaging(update, context):
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(callback_auto_message, 900, context=chat_id, name=str(chat_id))
    context.bot.send_message(chat_id=chat_id, text='Włączono powiadomienia o lądujących samolotach (15minut)')
    try:
        context.bot.send_message(chat_id=chat_id, text=getf())
    except:
        context.bot.send_message(chat_id=chat_id, text="Brak samolotów w pobliżu")
        pass


def start_auto_messaging2(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text='Włączono powiadomienia o lądujących samolotach (25minut)')
    context.job_queue.run_repeating(callback_auto_message, 1500, context=chat_id, name=str(chat_id))
    try:
        context.bot.send_message(chat_id=chat_id, text=getf())
    except:
        context.bot.send_message(chat_id=chat_id, text="Brak samolotów w pobliżu")
        pass

def stop_notify(update, context):
    chat_id = update.message.chat_id
    try:
        job = context.job_queue.get_jobs_by_name(str(chat_id))
        job[0].schedule_removal()
        context.bot.send_message(chat_id=chat_id, text='Wyłączono powiadomienia')
    except:
        context.bot.send_message(chat_id=chat_id, text='Brak powiadomień')

if __name__ == '__main__':
    updater = Updater('5656552566:AAG7JWW_zp7jB29b9-xqY7o0MwlVmLTYH40', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('auto', start_auto_messaging))
    dp.add_handler(CommandHandler('auto2', start_auto_messaging2))
    dp.add_handler(CommandHandler('stop', stop_notify))

    updater.start_polling(1.0)
    updater.idle()

