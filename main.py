import asyncio

import requests
from telebot.async_telebot import AsyncTeleBot

from bs4 import BeautifulSoup

from PrivateConfig import BOT_KEY_API, FB_ID, FB_SECRET, TOKEN_FB_60DAYS
from instagramAPI.RequestsAPI import getUserInfo, getLongToken, getAllPost

bot = AsyncTeleBot(f"{BOT_KEY_API}")

# states (none, setToken)
SET_TOKEN = "setToken"
SET_NONE = "none"
#
userState = "none"
userToken = ""

param = dict()


@bot.message_handler(commands=['start', 'help'])
async def initialCommands(message):
    if message.text == "/start":
        await bot.reply_to(message, "Hello, use /help to get all commands")
    else:
        await bot.reply_to(message, "/set_token - sets your personal token to communicate with instagram account\n"
                                    "/get_user - returns user (id, name)\n"
                                    "/get_all_post - get all post for all time")


# @bot.message_handler(commands=['set_token'])
# async def setToken(message):
#     global userState
#     userState = SET_TOKEN
#     await bot.reply_to(message, "input your token:")


@bot.message_handler(commands=['get_user'])
async def getUser(message):
    try:
        result = getUserInfo()
        await bot.send_message(message.chat.id, f"{result}")
    except Exception as e:
        print("exception when get user{0}".format(e))


@bot.message_handler(commands=['get_all_post'])
async def getAllMedia(message):
    try:
        result = getAllPost()
        await bot.send_message(message.chat.id, f"{result}")
    except Exception as e:
        print("exception when get user{0}".format(e))


# @bot.message_handler(func=lambda m: userState is SET_TOKEN)
# async def setToken(message):
#     global userToken, userState
#     userState = SET_NONE
#     print(getLongToken(message.text))


if __name__ == '__main__':
    try:
        asyncio.run(bot.polling(non_stop=True, request_timeout=90))
    except:
        print("except")
