from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.constants import GREETING_MESSAGE
import src.keyboard as kb
from src.states import OrderMenuStates
router_menu = Router()


@router_menu.message(CommandStart())
async def start_message(message: types.Message, state: FSMContext):
    user = message.from_user

    print(f"User ID: {user.id}")
    print(f"Username: @{user.username}")
    await message.answer(f"{user.first_name}{GREETING_MESSAGE}", reply_markup=kb.return_menu)
    await state.set_state(OrderMenuStates.main_menu)


@router_menu.message(OrderMenuStates.main_menu)
async def order_menu(message: types.Message, state: FSMContext):
    await message.answer("Выберите пункт меню", reply_markup=kb.markup)
    await state.clear()


@router_menu.callback_query(lambda call: call.data.startswith('menu'))
async def menu(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Выберите пункт меню", reply_markup=kb.markup)
    await state.clear()


@router_menu.callback_query(lambda call: call.data.startswith('add_products'))
async def process_callback_add(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Предистория, как добавлять продукты",
                                        reply_markup=ReplyKeyboardRemove())
    await callback_query.message.answer("Выберите, как вы хотите добавить продукты?",
                                        reply_markup=kb.add_product)
    await state.clear()








