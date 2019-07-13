import asyncio
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

BOT_TOKEN = "368667419:AAEFZdCFtjdPSYwVSURZVzso8tGgAcziggA"  # Insert token

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
loop = asyncio.get_event_loop()

bot = Bot(BOT_TOKEN, loop=loop, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)

if __name__ == '__main__':
    from handlers import *

    executor.start_polling(dp, skip_updates=True)
