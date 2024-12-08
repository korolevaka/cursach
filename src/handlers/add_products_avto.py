import pytesseract
from aiogram import types, Router, F
from aiogram.types import ContentType
from PIL import Image
import aiofiles
from io import BytesIO
import re

router_avto = Router()

@router_avto.callback_query(lambda call: call.data.startswith('automatically'))
async def add_products_avto(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Выбран авто ввод")

