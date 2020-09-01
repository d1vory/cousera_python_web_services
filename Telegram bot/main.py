import telebot
from collections import defaultdict

#restaraunt has name and place


token = '1188055161:AAGe2cINTEu-gb6eALnVMgvRKs-iRSsEADg'

bot = telebot.TeleBot(token)

ADD_START, ADD_NAME, ADD_PHOTO, ADD_LOCATION, ADD_CONFIRMATION, RELATIVE_LOCATION = range(6)
user_state = defaultdict(lambda:ADD_START)

def get_state(message):
	return user_state[message.chat.id]


def update_state(message, state):
	user_state[message.chat.id] = state



@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, 'Hello world!')

@bot.message_handler(commands=['add'])
def add_command(message):
    update_state(message, ADD_START)
    add_start(message)

@bot.message_handler(func= lambda m: get_state(m) == ADD_START)
def add_start(message):
    bot.send_message(message.chat.id, 'Write name of the place: ')
    update_state(message , ADD_NAME)


@bot.message_handler(func= lambda m: get_state(m) == ADD_NAME)
def add_name(message):
    bot.send_message(message.chat.id, 'Then send location of place')
    update_state(message , ADD_NAME)




@bot.message_handler(commands=['list'])
def list_command(message):
    bot.send_message(message.chat.id, 'list')

@bot.message_handler(commands=['reset'])
def reset_command(message):
    bot.send_message(message.chat.id, 'reset')


bot.polling()