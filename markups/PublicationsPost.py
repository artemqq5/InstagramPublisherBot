from telebot import types


def selectTypePost():
    markup = types.InlineKeyboardMarkup()

    listButtons = (
        types.InlineKeyboardButton('Image', callback_data="img_post"),
        types.InlineKeyboardButton('Ring Galleries', callback_data="ring_gallery_post"),
    )

    for i in listButtons:
        markup.add(i)

    return markup


def nextStepGallery():
    return types.ReplyKeyboardMarkup().add(types.KeyboardButton('Next'))


def closeMarkup():
    return types.ReplyKeyboardRemove(selective=False)
