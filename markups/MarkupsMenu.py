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


def selectTypeStatistic():
    markup = types.InlineKeyboardMarkup()

    listButtons = (
        types.InlineKeyboardButton('Impressions', callback_data="impressions"),
        types.InlineKeyboardButton('Reach', callback_data="reach"),
        types.InlineKeyboardButton('Profile Views', callback_data="profile_views"),
        types.InlineKeyboardButton('Followers', callback_data="follower_count"),
        types.InlineKeyboardButton('Website Clicks', callback_data="website_clicks"),  #  /insights?metric=website_clicks&period=day
        types.InlineKeyboardButton('Total Interactions', callback_data="total_interactions"), #
        types.InlineKeyboardButton('Likes', callback_data="likes"),  #
        types.InlineKeyboardButton('Comments', callback_data="comments"),  #
        types.InlineKeyboardButton('Shares', callback_data="shares"),  #
        types.InlineKeyboardButton('Saves', callback_data="saves"),  #
        types.InlineKeyboardButton('Replies', callback_data="replies"), #  /insights?metric=replies&metric_type=total_value&period=day
    )

    for i in listButtons:
        markup.add(i)

    return markup


def closeMarkup():
    return types.ReplyKeyboardRemove(selective=False)

