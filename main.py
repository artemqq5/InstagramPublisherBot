import asyncio
import io
import threading

import requests
from markups.MarkupsMenu import selectTypePost, nextStepGallery, closeMarkup, selectTypeStatistic
from telebot.async_telebot import AsyncTeleBot

from DataBase.UserQuery import createUser, getUser, updateToken
from Messages import *
from PrivateConfig import BOT_KEY_API
from instagramAPI.MediaDataParse import parseAllPosts
from instagramAPI.RequestsAPI import getAllPost, getLongToken, createContainerMEDIA, publishMEDIA, getAccountInfo, \
    getStatistic

bot = AsyncTeleBot(f"{BOT_KEY_API}")

# states (none, setToken)
SET_TOKEN = "SET_TOKEN"
STATE_NONE = "NONE"
CREATE_CONTAINER_IMG = "CREATE_CONTAINER_POST_IMG"
CREATE_CONTAINER_IMG_GALLERY = "CREATE_CONTAINER_POST_GALLERY_IMG"
#
userState = STATE_NONE
userCommands = ("/start", "/help", "/set_token", "/get_all_posts", "/publish_post", "/account", "/statistic")

operationCounter = {"counterStep": 0}  # counter steps into some operations
localDataList = {}  # list to save temporary data
listContainersPublicationsID = []  # list for several objects in one post like CAROUSEL


@bot.message_handler(commands=['start', 'help'])
async def initialCommands(message):
    global userState
    userState = STATE_NONE

    if message.text == "/start":
        # check if user not registered to register him
        if getUser(message.chat.id) is None:
            createUser(message.chat.id)

        await bot.send_message(message.chat.id, START_MESSAGE, reply_markup=closeMarkup())
    else:
        await bot.send_message(message.chat.id, HELP_MESSAGE, reply_markup=closeMarkup())


@bot.message_handler(commands=['set_token'])
async def setToken(message):
    global userState
    userState = SET_TOKEN

    await bot.reply_to(message, "Input your token:")


@bot.message_handler(func=lambda m: userState is SET_TOKEN and m.text not in userCommands)
async def getToken(message):
    global userState
    userState = STATE_NONE

    try:  # if response get code 400, field `access_token` haven't and throw exception
        result = getLongToken(message.text)['access_token']
        updateToken(result, message.chat.id)
        await bot.send_message(message.chat.id, SUCCESSFUL_GENERATE_TOKEN)
    except Exception as e:
        print(f"except when generate long token {e}")
        if getUser(message.chat.id) is None:
            await bot.send_message(message.chat.id, YOU_NEED_REGISTER)
        else:
            await bot.send_message(message.chat.id, CHECK_ACCESS_TOKEN)


@bot.message_handler(commands=['statistic'])
async def getUserInfo(message):
    global userState
    userState = STATE_NONE
    user = getUser(message.chat.id)

    if user is not None:
        await bot.send_message(message.chat.id, "Select type of statistic", reply_markup=selectTypeStatistic())
    else:
        await bot.send_message(message.chat.id, EXCEPTION_AUTHORISATION)


@bot.message_handler(commands=['account'])
async def getUserInfo(message):
    global userState
    userState = STATE_NONE
    user = getUser(message.chat.id)

    if user is not None:
        result = getAccountInfo(user.token)
        result_data = result.json()
        if result.status_code == 200:
            photo = io.BytesIO(requests.get(result_data['profile_picture_url']).content)
            text = f"id: {result_data['id']}\n" \
                   f"name: {result_data['name']}\n" \
                   f"username: {result_data['username']}\n" \
                   f"biography: {result_data['biography']}\n" \
                   f"website: {result_data['website']}\n" \
                   f"media: {result_data['media_count']}\n" \
                   f"follows: {result_data['follows_count']}\n" \
                   f"followers: {result_data['followers_count']}\n"

            await bot.send_photo(message.chat.id, caption=text, photo=photo)
        else:
            text = result_data['error']['message']
            await bot.send_message(message.chat.id, text)
    else:
        await bot.send_message(message.chat.id, EXCEPTION_AUTHORISATION)


@bot.message_handler(commands=['get_all_posts'])
async def getAllMedia(message):
    global userState
    userState = STATE_NONE

    try:  # if response get code 400, field `data` haven't and throw exception
        result = getAllPost(getUser(message.chat.id).token)
        for post in parseAllPosts(result):
            await bot.send_photo(message.chat.id, photo=post.img, caption=post.desc)

    except Exception as e:
        await bot.send_message(message.chat.id, GET_MEDIA_EXCEPTION)
        print(f"exception when getAllPost {e}")


@bot.message_handler(commands=['publish_post'])
async def publishPost(message):
    global userState
    userState = STATE_NONE

    if getUser(message.chat.id) is not None:
        await bot.send_message(message.chat.id, "Select type of publication", reply_markup=selectTypePost())
    else:
        await bot.send_message(message.chat.id, EXCEPTION_AUTHORISATION)


@bot.message_handler(func=lambda m: userState == CREATE_CONTAINER_IMG)
async def createIMGContainer(message):
    global userState

    match operationCounter["counterStep"]:
        case 1:
            operationCounter["counterStep"] = 2
            localDataList["image_url"] = message.text
            await bot.send_message(message.chat.id, "Input caption : ")
        case 2:
            localDataList["caption"] = message.text
            #
            try:
                await publishLazyPost(
                    message.chat.id,
                    createContainerMEDIA(getUser(message.chat.id).token, localDataList)['id']
                )
            except Exception as e:
                print(f"exception when Create IMG publication: {e}")
                await bot.send_message(message.chat.id, EXCEPT_CREATE_POST)
                userState = STATE_NONE


@bot.message_handler(func=lambda m: userState == CREATE_CONTAINER_IMG_GALLERY)
async def createIMGGalleryContainer(message):
    global userState

    match operationCounter["counterStep"]:
        case 1:
            if len(listContainersPublicationsID) < 10 and message.text != "Next":
                print(len(listContainersPublicationsID))
                localDataList["image_url"] = message.text
                try:
                    listContainersPublicationsID.append(
                        createContainerMEDIA(getUser(message.chat.id).token, localDataList)['id']
                    )
                except Exception as e:
                    print(f"{EXCEPT_ADD_IMG}: {e}")
                    await bot.send_message(message.chat.id, EXCEPT_ADD_IMG)
                await bot.send_message(message.chat.id, "Input URL to set img : ", reply_markup=nextStepGallery())
            else:
                operationCounter["counterStep"] = 2
                await bot.send_message(message.chat.id, "Input caption : ", reply_markup=closeMarkup())
        case 2:
            localDataList.clear()
            localDataList['media_type'] = 'CAROUSEL'
            localDataList['caption'] = message.text
            localDataList['children'] = listContainersPublicationsID
            try:
                await publishLazyPost(
                    message.chat.id,
                    createContainerMEDIA(getUser(message.chat.id).token, localDataList)['id']
                )
            except Exception as e:
                print(f"exception when Create Gallery IMG publication: {e}")
                await bot.send_message(message.chat.id, EXCEPT_CREATE_POST)
                userState = STATE_NONE


@bot.callback_query_handler(
    func=lambda call: call.data in ["img_post", "ring_gallery_post"])
async def publicationCallBackHandler(call):
    global userState
    userState = STATE_NONE  # clear user state
    operationCounter["counterStep"] = 1  # clear operation list before new operations
    localDataList.clear()  # clear local temporary list data before new operations

    if getUser(call.from_user.id) is not None:
        match call.data:
            case "img_post":
                userState = CREATE_CONTAINER_IMG
                await bot.send_message(call.from_user.id, "Input URL to set img : ")
            case "ring_gallery_post":
                localDataList["is_carousel_item"] = 'true'
                userState = CREATE_CONTAINER_IMG_GALLERY
                await bot.send_message(call.from_user.id, "Input URL to set img : ")
            case _:
                pass
    else:
        await bot.send_message(call.from_user.id, EXCEPTION_AUTHORISATION)


@bot.callback_query_handler(
    func=lambda call: call.data in ["impressions", "reach", "profile_views", "follower_count", "website_clicks",
                                    "total_interactions", "likes", "comments", "shares", "saves", "replies"])
async def statisticCallBackHandler(call):
    global userState
    userState = STATE_NONE  # clear user state

    user = getUser(call.from_user.id)
    if user is not None:
        match call.data:
            case "impressions" | "reach" | "profile_views" | "follower_count" | "website_clicks":
                try:
                    res = getStatistic(user.token, call.data)
                    if len(res['data']) != 0:
                        value = res['data'][0]['values'][0]['value'] + res['data'][0]['values'][1]['value']
                        text = res['data'][0]['description']
                        await bot.send_message(call.from_user.id, f"{text}\n\n{value}")
                    else:
                        await bot.send_message(call.from_user.id, "no data")

                except Exception as e:
                    print(f"exception statisticCallBackHandler {e}")
            case "total_interactions" | "likes" | "comments" | "shares" | "saves" | "replies":
                try:
                    res = getStatistic(user.token, call.data, True)
                    print(res)
                    if len(res['data']) != 0:
                        value = res['data'][0]['total_value']['value']
                        text = res['data'][0]['description']
                        await bot.send_message(call.from_user.id, f"{text}\n\n{value}")
                    else:
                        await bot.send_message(call.from_user.id, "no data")
                except Exception as e:
                    print(f"statisticCallBackHandler {e}")
                pass
    else:
        await bot.send_message(call.from_user.id, EXCEPTION_AUTHORISATION)


async def publishLazyPost(chat_id, id_post):
    listContainersPublicationsID.clear()

    await asyncio.sleep(10)  # time to load img in instagram

    try:
        result_published = publishMEDIA(
            getUser(chat_id).token, id_post
        )['id']  # to check result if no 'id' throw exc

        await bot.send_message(chat_id, f"Post just have published!\nid: {result_published}")
    except Exception as e:
        print(f"exception when Create IMG publication: {e}")
        await bot.send_message(chat_id, EXCEPT_CREATE_POST)


if __name__ == '__main__':
    try:
        asyncio.run(bot.polling(non_stop=True, request_timeout=90))
    except Exception as exc:
        print(f"except in bot {exc}")
