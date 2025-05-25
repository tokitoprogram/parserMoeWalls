from functions import parser, DownloadWallpaper
import schedule, time, datetime, os, logging, asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F
from dotenv import load_dotenv
load_dotenv(".env")
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    kb = [
        [KeyboardButton(text="Сменить обойку")],
        [KeyboardButton(text="Фильтры")],
        [KeyboardButton(text="Сменить сайт")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(
                        "**Привет!**. \n"
                        "Этот бот создан чтобы скачивать рандом анимированые обойки каждый день, \n"
                        "А вот и инструкция: \n"
                        "Чтобы скачать рандом анимированную обойку без фильтров нажмите **Сменить обойку** \n"
                        "Чтобы добавить фильтры, категорию нажмите **Фильтры**\n"
                        "Чтобы поменять сайт нажмите **Сменить сайт** \n"
                        "И наконец информация на \n"
                        , reply_markup=keyboard)

@dp.message(F.text.lower()=="Сменить обойку")
async def command_wallpaperRandom_handler(message: Message):
    DownloadWallpaper()












async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())