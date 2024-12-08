from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

import src.keyboard as kb
import src.database as db

from src.states import EditProduct

router_get = Router()


# формирование карточки продукта
def create_product_card(product, product_id):
    product_details = (
        f"*Название:* {product.product}\n"
        f"*Количество:* {product.quantity} {product.quantity_unit}\n"  # Добавляем единицу измерения
        f"*Дата изготовления:* {product.production_date.strftime('%Y-%m-%d')}\n"
        f"*Годен до:* {product.expiry_date.strftime('%Y-%m-%d')}\n"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Редактировать", callback_data=f"edit_product_{product_id}"),
                InlineKeyboardButton(text="Удалить", callback_data=f"delete_product_{product_id}"),
            ],
            [InlineKeyboardButton(text="Закрыть", callback_data="close_card")]
        ]
    )
    return product_details, keyboard


# список продуктов
async def display_product_list(user_id, message):
    products = db.get_products(user_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                            [InlineKeyboardButton(text=product.product, callback_data=f"view_product_{product.id}")]
                            for product in products
                        ] + [[InlineKeyboardButton(text="Вернуться в меню", callback_data="menu")]]
    )
    await message.answer("Выберите продукт для просмотра:", reply_markup=keyboard)


# Обработчик отображения списка продуктов
@router_get.callback_query(lambda call: call.data.startswith('view_products'))
async def process_callback_view(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await display_product_list(user_id, callback_query.message)


# Обработчик для отображения карточки продукта
@router_get.callback_query(lambda call: call.data.startswith('view_product_'))
async def process_view_product(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data.split("_")[-1])
    product = db.get_product_by_id(product_id)

    if not product:
        await callback_query.answer("Продукт не найден.", show_alert=True)
        return

    product_details, keyboard = create_product_card(product, product_id)
    await callback_query.message.edit_text(product_details, reply_markup=keyboard)


# Обработчик нажатия кнопки "Редактировать"
@router_get.callback_query(lambda call: call.data.startswith('edit_product_'))
async def process_edit_product(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = int(callback_query.data.split("_")[-1])
    await state.update_data(product_id=product_id)
    await callback_query.message.edit_text("Что вы хотите изменить?", reply_markup=kb.product_edit)


# Обработчик выбора редактируемого параметра
@router_get.callback_query(lambda call: call.data in [
    "edit_name", "edit_quantity", "edit_production_date", "edit_expiry_date"])
async def handle_edit_choice(callback_query: types.CallbackQuery, state: FSMContext):
    choice = callback_query.data
    await state.update_data(edit_choice=choice)

    prompts = {
        "edit_name": "Введите новое название продукта:",
        "edit_quantity": "Введите новое количество (число):",
        "edit_production_date": "Введите новую дату изготовления (в формате YYYY-MM-DD):",
        "edit_expiry_date": "Введите новый срок годности в днях:"
    }

    await state.set_state(EditProduct.choice)
    await callback_query.message.edit_text(prompts[choice])


# Обработчик ввода нового значения
@router_get.message(EditProduct.choice)
async def handle_edit_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product_id = data["product_id"]
    edit_choice = data["edit_choice"]
    new_value = message.text.strip()

    if edit_choice == "edit_name":
        db.update_product_name(product_id, new_value)
    elif edit_choice == "edit_quantity":
        if not new_value.replace('.', '', 1).isdigit():
            await message.reply("Количество должно быть числом. Попробуйте еще раз.")
            return
        db.update_product_quantity(product_id, float(new_value))
    elif edit_choice == "edit_production_date":
        try:
            new_production_date = datetime.datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            await message.reply("Неверный формат даты. Используйте формат YYYY-MM-DD.")
            return
        db.update_product_production_date(product_id, new_production_date)
    elif edit_choice == "edit_expiry_date":
        if not new_value.isdigit():
            await message.reply("Срок годности должен быть числом. Попробуйте еще раз.")
            return
        new_expiry_days = int(new_value)
        db.update_product_expiry_days(product_id, new_expiry_days)

    product = db.get_product_by_id(product_id)
    if product:
        product_details, keyboard = create_product_card(product, product_id)
        await message.answer(product_details, reply_markup=keyboard)

    await state.clear()


# Обработчик отмены редактирования
@router_get.callback_query(lambda call: call.data == "cancel_edit")
async def cancel_edit(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text("Редактирование отменено.")


# Обработчик удаления продукта
@router_get.callback_query(F.data.startswith('delete_product_'))
async def process_delete_product(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data.split("_")[-1])
    db.delete_product(product_id)
    await callback_query.answer("Продукт удален.")
    await display_product_list(callback_query.from_user.id, callback_query.message)


# Обработчик закрытия карточки
@router_get.callback_query(F.data == "close_card")
async def close_product_card(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await display_product_list(callback_query.from_user.id, callback_query.message)
