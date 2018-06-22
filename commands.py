import datetime
import random
from functools import lru_cache

import spotipy
from emoji import emojize
from requests import get
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import Message, ParseMode

from data import julien, days, ayuda
from helpers.imdb import get_rating_by_id, get_rating_by_title

SPOTIPY_CLIENT_ID = '0f9f9324ddd54895848e32fe5cea0d47'
SPOTIPY_CLIENT_SECRET = 'e6a9ce6a89ed4196a83e3fc65709ccc0'
client_credentials = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                              client_secret=SPOTIPY_CLIENT_SECRET)

SAVED_MESSAGE_LIST_IS_EMPTY_MESSAGE = "No hay mensajes guardao' mi loki"


def Start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='SOY GIRU MANIN!! Dale "/ayuda".')


def Caps(bot, update, args):
    text = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text + '!')


def create_get_saved_messages_callback(storage_provider):
    def get_saved_messages_callback(bot, update):
        replies = storage_provider.get_all_replies()

        def format_saved_message(message):  # type: (Message) -> str
            return '*{}* - [{}](tg://user?id={})'.format(message.text, message.from_user.first_name,
                                                         message.from_user.id)

        formatted_replies = list(map(format_saved_message, replies))

        text = '\n'.join(formatted_replies) if formatted_replies else SAVED_MESSAGE_LIST_IS_EMPTY_MESSAGE

        bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN)

    return get_saved_messages_callback


def Julien(bot, update):
    sel = random.choice(julien)
    # cal = InputMediaPhoto(sel, 'Julien')
    bot.sendPhoto(chat_id=update.message.chat_id, photo=sel)


def Spotify(bot, update, args):
    query = ' '.join(args).lower()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials)
    results = sp.search(q='' + query, type='track', limit=1)
    if results['tracks']['items']:
        artist = results['tracks']['items'][0]['artists'][0]['name']
        song = results['tracks']['items'][0]['name']
        audio = results['tracks']['items'][0]['preview_url']
        url = results['tracks']['items'][0]['external_urls']['spotify']
        message = emojize('*' + artist + '* - [' + song + '](' + url + ') ' + ':notes:', use_aliases=True)
        bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')
        if audio:
            bot.sendAudio(chat_id=update.message.chat_id, audio=audio)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=emojize(':x:', use_aliases=True) + ' No hay preview.', parse_mode='Markdown')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='No encuentro la cancion bi.', parse_mode='Markdown')


@lru_cache()
def cached_padondehoy_response(date, chat):
    day_of_week = date.weekday()
    return random.choice(days[day_of_week])


def PaDondeHoy(bot, update):
    date = datetime.date.today()
    response = cached_padondehoy_response(date, update.message.chat_id)
    bot.sendMessage(chat_id=update.message.chat_id, text=response)


def Ayuda(bot, update):
    """ Sends a list of the commands and their use. """
    message = 'Hola, soy Giru.\n\n*Comandos:* \n'
    for k in sorted(ayuda):
        message += '%s: ' % k
        for k2, i in ayuda[k].items():
            message += '%s\n\t- Ejemplo: _%s_\n' % (k2, i)
    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')


def Cartelera(bot, update):
    """ Get's all the movies in theathers right now. """
    movies = get('http://api.cine.com.do/v1/movies').json()

    message = '*Cartelera al día {0}:*\n\n'.format(datetime.datetime.today().strftime('%d-%m-%Y'))

    for m in movies:
        if m.get('published') and not m.get('comingsoon'):
            imdb_string = ''

            if m.get('imdbScore'):
                if m.get('imdbId'):
                    imdb_string = "[{}]({})".format(m.get('imdbScore'),
                                                    "https://www.imdb.com/title/" + m.get('imdbId'))
                else:
                    imdb_string = m.get('imdbScore')
            else:

                if m.get('imdbId'):
                    imdb_string = "[{}]({})".format(get_rating_by_id(m.get('imdbId')),
                                                    "https://www.imdb.com/title/" + m.get('imdbId'))
                else:
                    result = get_rating_by_title(m.get('title'))
                    if result:
                        rating, imdburl = result
                        imdb_string = "[{}]({})".format(rating, imdburl)

            message += '[{}]({}) *{}*\n'.format(m.get('title'),
                                                "http://www.cine.com.do/peliculas/" + m.get('slug'),
                                                imdb_string)

    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown', disable_web_page_preview=True)
