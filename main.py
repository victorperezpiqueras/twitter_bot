#!/usr/bin/env python3

"""Requisitos:
Crear un bot en Telegram con @BotFather.
Crear un canal publico y meter al bot como administrador.
Obtener id del canal publico haciendo llamada http GET a https://api.telegram.org/bot<bot_token>/getUpdates
en response.result.message.chat.id
"""
from dotenv import load_dotenv

load_dotenv()
import os


import requests
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream

bot_token = os.environ.get("bot_token")  # Token del bot que da @BotFather
bot_chatID = os.environ.get(
    "bot_chat_id"
)  # ID del usuario al que quieras enviar mensajes o del canal
twitter_account_id = os.environ.get(
    "twitter_account_id"
)  # ID del usuario de twitter al que escuchar
twitter_account_id2 = os.environ.get(
    "twitter_account_id2"
)  # ID del usuario de twitter al que escuchar

twitter_consumer_api_key = os.environ.get(
    "twitter_consumer_api_key"
)  # api key de la app de twitter
twitter_consumer_api_secret_key = os.environ.get(
    "twitter_consumer_api_secret_key"
)  # api key secret de la app de twitter
twitter_access_token = os.environ.get("twitter_access_token")  # token acceso twitter
twitter_access_token_secret = os.environ.get(
    "twitter_access_token_secret"
)  # token secret acceso twitter


def telegram_bot_sendtext(bot_token, bot_chatID, bot_message, bot_message2):
    # PETICION A LA API
    r = requests.post(
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
        "Usuario: " + bot_message + "\nTweet:" + bot_message2
    )


class StdOutListener(StreamListener):
    def on_status(self, status):
        # if status.user.id_str != twitter_account_id and status.user.id_str !=twitter_account_id2:
        #   return

        # evitar comentar retweets
        if hasattr(status, "retweeted_status"):
            return

        print(status.text)
        # print(status)
        telegram_bot_sendtext(
            bot_token, bot_chatID, status.user.screen_name, status.text
        )
        # print(status.id)
        imagePath = "vegetta.jpg"

        status_msg = "@" + status.user.screen_name
        api.update_with_media(
            filename=imagePath, status=status_msg, in_reply_to_status_id=status.id
        )

    def on_error(self, status_code):
        print(status_code)


palabras_track = [
    "andorrano",
]

if __name__ == "__main__":
    print("imbecil_bot iniciado")
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(
        twitter_consumer_api_key, twitter_consumer_api_secret_key
    )
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth)

    # LANZAR EL STREAM LISTENER Y FILTRAR
    stream = Stream(auth, listener)
    stream.filter(track=palabras_track)