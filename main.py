from os import environ
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from dotenv import load_dotenv
from aiohttp import ClientSession
from aiobalaboba import Balaboba

load_dotenv()  # load env file
logging.basicConfig(level=logging.INFO)  # set logging

# base vars for bot
bot = Bot(token=environ.get("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    return await message.reply(
        f"Привет, {message.from_user.mention}! Введи текст для того, чтобы сгенерировать его продолжение с помощью нейросетей!")


@dp.message_handler()
async def execute_action(message: Message):
    if message.text == "/start":
        return await start_command(message)
    msg = await message.reply("Подождите, скоро будет готово...")
    bb = Balaboba()
    data = await bb.balaboba(query=message.text, intro=0)
    if data is None:
        return await msg.reply("Что-то пошло не так...\nПопробуйте еще раз.")
    await msg.reply(data)


if __name__ == "__main__":
    executor.start_polling(dp)
