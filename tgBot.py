import asyncio
import TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
import emoji
import parseTable
import re
bot = Bot(token=TOKEN.tokenTG)
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start","help"])
async def start(message: types.Message):
    await message.answer(emoji.emojize(":grinning_face: ")+"Добро пожаловать в чат-бота для Новодеревеньковского районного суда п. Хомутово\n"+\
                         emoji.emojize(":backhand_index_pointing_right: ")+"Вы можете просмотреть список дел, назначенных к слушанию на определенную дату!\n"+\
                         emoji.emojize(":backhand_index_pointing_right: ")+"Введите интересующую Вас дату слушания, а я пришлю список дел!\n"+\
                         emoji.emojize(":green_square: ")+"ВАЖНО: дату вводить в формате dd.mm.yyyy, т.е., например 24.01.2022\n"+ \
                         emoji.emojize(":green_square: ")+"Для помощи напишите /help"
                         )

@dp.message_handler(commands="block")
async def cmd_block(message: types.Message):
    await asyncio.sleep(10.0)
    await message.reply(emoji.emojize(":warning: ")+"Вы заблокированы")
'''
@dp.message_handler(regexp='(0[1-9]|[12][0-9]|3[01])[- ..](0[1-9]|1[012])[- ..](19|20)\d\d')
async def data(message: types.Message):
    for item in parseTable.getData(message.text):
        await message.answer(item)
'''

@dp.message_handler()
async def echo(message: types.Message):
    regexpr = "(0[1-9]|[12][0-9]|3[01])[- ..](0[1-9]|1[012])[- ..](19|20)\d\d"
    if re.match(regexpr, message.text) is not None:
        for item in parseTable.getData(message.text):
            await message.answer(item)
    else:
        await message.answer(emoji.emojize(":green_square: ")+"ВАЖНО: дату вводить в формате dd.mm.yyyy, т.е., например 24.01.2022\n")

if __name__ == '__main__':
   executor.start_polling(dp)