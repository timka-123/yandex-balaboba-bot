from os import environ
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv
from aiohttp import ClientSession
from aiobalaboba import Balaboba

load_dotenv()  # load env file
logging.basicConfig(level=logging.INFO)  # set logging

# base vars for bot
bot = Bot(token=environ.get("TOKEN"))
dp = Dispatcher(bot)
global text


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    return await message.reply(
        f"Привет, {message.from_user.mention}! Введи текст для того, чтобы сгенерировать его продолжение с помощью нейросетей!")

@dp.message_handler()
async def execute_action(message: Message):
    view = InlineKeyboardMarkup(row_width=2)
    nonestyle = InlineKeyboardButton(text="Без стиля", callback_data="0")
    howto = InlineKeyboardButton(text="Иннструкция к применению", callback_data='24')
    recipe = InlineKeyboardButton(text="Рецепты", callback_data='25')
    narod = InlineKeyboardButton(text="Народная мудрость", callback_data='11')
    short = InlineKeyboardButton(text="Короткие истории", callback_data='6')
    wiki = InlineKeyboardButton(text="Короче, Википедия", callback_data='8')
    film = InlineKeyboardButton(text="Синопсисы к фильму", callback_data='9')
    sport = InlineKeyboardButton(text="Балабоба и sports.ru", callback_data='34')
    love = InlineKeyboardButton(text="Песни о любви", callback_data="37")
    view.add(nonestyle, howto, recipe, narod, short, wiki, film, sport, love)
    global text
    text = message.text
    await message.reply("Выберите категорию генерации", reply_markup=view)


@dp.callback_query_handler()
async def type_handler(query: CallbackQuery):
    bb = Balaboba()
    global text
    if text is None:
        return await query.answer("Извините, но вызовите данную интеракцию снова, чтобы использовать её", show_alert=True)
    await query.answer("Ожидайте ответа от нейросети.", show_alert=True)
    data = await bb.balaboba(query=str(text), intro=int(query.data))
    if data == text:
        return await query.message.reply("Извините, но Балабоба не смогла обработать данный запрос.")
    text = None
    return await query.message.reply(f"{data}\n\nСоздано с помощью @yandex_balaboba_bot")


if __name__ == "__main__":
    executor.start_polling(dp)
