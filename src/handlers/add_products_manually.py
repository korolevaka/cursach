import datetime

from aiogram import types, F, Router
import re
from aiogram.fsm.context import FSMContext

import src.keyboard as kb
import src.database as db
from src.states import AddProduct

router_manually = Router()

# Регулярные выражения для валидации
NAME_REGEX = re.compile(r"^[a-zA-Zа-яА-Я0-9\s\-]{2,50}$")  # Название продукта
DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # Формат даты
INTEGER_REGEX = re.compile(r"^\d+$")  # Целое число


@router_manually.callback_query(lambda call: call.data.startswith('manually'))
async def add_products_manual(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Введите название продукта:")
    await state.set_state(AddProduct.product_name)


@router_manually.message(AddProduct.product_name, F.text)
async def process_product_name(message: types.Message, state: FSMContext):
    product_name = message.text.strip()
    if not NAME_REGEX.match(product_name):
        await message.answer("Название продукта не может быть пустым. Попробуйте снова:")
        return
    await state.update_data(product_name=product_name)
    await message.answer("Введите количество:")
    await state.set_state(AddProduct.quantity)


@router_manually.message(AddProduct.quantity, F.text)
async def process_quantity(message: types.Message, state: FSMContext):
    quantity = message.text.strip()
    if not INTEGER_REGEX.match(quantity) or float(quantity) <= 0:
        await message.answer("Некорректное количество. Укажите положительное число:")
        return

    await state.update_data(quantity=float(quantity))
    await message.answer("Введите единицу измерения (например, кг, шт, л):")
    await state.set_state(AddProduct.quantity_unit)


@router_manually.message(AddProduct.quantity_unit, F.text)
async def process_quantity_unit(message: types.Message, state: FSMContext):
    quantity_unit = message.text.strip()
    if not quantity_unit:
        await message.answer("Единица измерения не может быть пустой. Попробуйте снова:")
        return

    await state.update_data(quantity_unit=quantity_unit)
    await message.answer("Введите дату производства (в формате ГГГГ-ММ-ДД):")
    await state.set_state(AddProduct.production_date)


@router_manually.message(AddProduct.production_date, F.text)
async def process_production_date(message: types.Message, state: FSMContext):
    production_date = message.text.strip()
    if not DATE_REGEX.match(production_date):
        await message.answer("Некорректная дата. Укажите дату в формате ГГГГ-ММ-ДД:")
        return
    try:
        production_date = datetime.datetime.strptime(production_date, "%Y-%m-%d").date()
        if production_date > datetime.date.today():
            raise ValueError("Дата производства не может быть в будущем.")
    except ValueError:
        await message.answer("Некорректная дата. Проверьте формат или укажите прошедшую дату:")
        return
    await state.update_data(production_date=production_date)
    await message.answer("Введите срок годности (в днях, положительное целое число):")
    await state.set_state(AddProduct.expiry_days)


@router_manually.message(AddProduct.expiry_days, F.text)
async def process_expiry_date(message: types.Message, state: FSMContext):
    expiry_days = message.text.strip()
    if not INTEGER_REGEX.match(expiry_days) or int(expiry_days) <= 0:
        await message.answer("Некорректный срок годности. Укажите положительное целое число:")
        return
    await state.update_data(expiry_days=int(expiry_days))
    data = await state.get_data()
    user = message.from_user
    user_id = user.id
    production_date = data.get("production_date")
    expiry_date = production_date + datetime.timedelta(days=data['expiry_days'])

    try:
        db.add_product(
            user_id,
            data['product_name'],
            data['quantity'],
            data['quantity_unit'],
            production_date,
            expiry_date,
            data['expiry_days']
        )
        await message.answer("Продукт добавлен!", reply_markup=kb.replay_product)
    except Exception as e:
        await message.answer(f"Произошла ошибка при добавлении продукта: {e}")
        return
    await state.clear()
