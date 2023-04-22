import asyncio

from telebot.async_telebot import AsyncTeleBot

from PrivateConfig import BOT_KEY_API

bot = AsyncTeleBot(f"{BOT_KEY_API}")


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    await bot.reply_to(message, "Howdy, how are you doing?")


if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))
