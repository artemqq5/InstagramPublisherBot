import asyncio
import io

import requests
from telebot.async_telebot import AsyncTeleBot

from DataBase.UserQuery import createUser, getUser, updateToken
from Messages import *
from PrivateConfig import BOT_KEY_API
from instagramAPI.MediaDataParse import parseAllPosts
from instagramAPI.RequestsAPI import getAllPost, getLongToken

bot = AsyncTeleBot(f"{BOT_KEY_API}")

# states (none, setToken)
SET_TOKEN = "setToken"
SET_NONE = "none"
#
userState = SET_NONE

userCommands = ("/start", "/help", "/set_token", "/get_all_posts")


@bot.message_handler(commands=['start', 'help'])
async def initialCommands(message):
    global userState
    userState = SET_NONE
    
    if message.text == "/start":

        # check if user not registered to register him
        if getUser(message.chat.id) is None:
            createUser(message.chat.id)

        await bot.reply_to(message, START_MESSAGE)
    else:
        await bot.reply_to(message, HELP_MESSAGE)


@bot.message_handler(commands=['set_token'])
async def setToken(message):
    global userState
    userState = SET_TOKEN

    await bot.reply_to(message, "Input your token:")


@bot.message_handler(func=lambda m: userState is SET_TOKEN and m.text not in userCommands)
async def getToken(message):
    global userState
    userState = SET_NONE

    try:  # if response get code 400, field `access_token` haven't and throw exception
        result = getLongToken(message.text)['access_token']
        updateToken(result, message.chat.id)
        await bot.send_message(message.chat.id, SUCCESSFUL_GENERATE_TOKEN)
    except Exception as e:
        await bot.send_message(message.chat.id, CHECK_ACCESS_TOKEN)
        print(f"except when generate long token {e}")


@bot.message_handler(commands=['get_all_posts'])
async def getAllMedia(message):
    global userState
    userState = SET_NONE

    try:  # if response get code 400, field `data` haven't and throw exception
        result = getAllPost(getUser(message.chat.id).token)
        for post in parseAllPosts(result):
            await bot.send_photo(message.chat.id, photo=post.img, caption=post.desc)
    except Exception as e:
        await bot.send_message(message.chat.id, GET_MEDIA_EXCEPTION)
        print(f"exception when getAllPost {e}")


if __name__ == '__main__':
    try:
        asyncio.run(bot.polling(non_stop=True, request_timeout=90))
    except Exception as exc:
        print(f"except in bot {exc}")
