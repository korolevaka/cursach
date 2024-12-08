import asyncio
import logging

from aiogram import Bot, Dispatcher

from src import config
from src.handlers.add_products_avto import router_avto
from src.handlers.add_products_manually import router_manually
from src.handlers.get_products import router_get
from src.handlers.order_menu import router_menu
from src.handlers.recipes import router_recept

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

TOKEN = config.TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router_menu)
dp.include_router(router_manually)
dp.include_router(router_get)
dp.include_router(router_recept)
dp.include_router(router_avto)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
