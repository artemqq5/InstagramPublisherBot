from telebot import types


def selectTypePost():
    markup = types.InlineKeyboardMarkup()

    listButtons = (
        types.InlineKeyboardButton('Image', callback_data="img_post"),
        # types.InlineKeyboardButton('Video', callback_data="video_post"),
        # types.InlineKeyboardButton('Reels', callback_data="reels_post"),
        # types.InlineKeyboardButton('Ring Galleries', callback_data="ring_galleries_post"),
    )

    for i in listButtons:
        markup.add(i)

    return markup
