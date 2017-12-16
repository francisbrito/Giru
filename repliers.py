import re
from telegram.ext import BaseFilter
from telegram import Message

saved = 'src/texts/saved.txt'

class FilterMmg(BaseFilter):
    def filter(self, message):
        found = re.search("(mmg)|(mamague(b|v))", message.text, re.IGNORECASE)
        # print(message)
        return found

def respondM(bot, update):
    """ Respond to a pattern in FilterMmg. """
    bot.sendMessage(chat_id=update.message.chat_id, text='MMG UTE!')

class FilterReply(BaseFilter):
    def filter(self, message):
        reply = message.reply_to_message
        if message.reply_to_message and message.text == '-save':
            with open(saved, 'a') as file:
                file.write('*' + reply.text + '* - [' + reply.from_user.first_name + '](tg://user?id=' \
                + str(reply.from_user.id) + ')\n')

def sdm(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Mensaje guardado.')

class FilterSalut(BaseFilter):
    def filter(self, message):
        found = re.search("(giru)", message.text, re.IGNORECASE)
        if found:
            return True

def salute(bot, update):
    if 'hola' or 'holi' in update.message.text.lower():
        bot.sendMessage(chat_id=update.message.chat_id, text='Hola!')
    elif 'klk' in update.message.text.lower():
        bot.sendMessage(chat_id=update.message.chat_id, text='Dime buen barrial.')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Dimelo.')
