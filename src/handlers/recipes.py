from aiogram import types, Router
from aiogram.fsm.context import FSMContext

import src.database as db
import requests
import json

import src.keyboard as kb
from src import config
from src.states import RecipeState

api_key = config.api_key
url = config.url

headers = {
    "Content-Type": "application/json"
}

params = {
    "key": api_key
}

router_recept = Router()


async def get_user_products(user_id):
    products = db.get_products(user_id)
    return [{"name": product.product, "quantity": product.quantity, "quantity_unit": product.quantity_unit} for product
            in products]


def generate_prompt(products, recipe_type=None):
    product_str = ", ".join([f"{prod['quantity']} {prod['quantity_unit']} {prod['name']}" for prod in products])
    prompt = f"Предложи 3 рецепта {recipe_type} , которые можно приготовить с такими ингредиентами: {product_str} (не обязательно использовать полное количество ингридиентов). Выведи: ингридиенты (разделив на имеющиеся и дополнительные), описание, инструкцию."
    return prompt


async def get_recipes_from_gpt(products, recipe_type=None):
    prompt = prompt = generate_prompt(products, recipe_type)
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    return data


@router_recept.callback_query(lambda call: call.data.startswith('show_recipes'))
async def process_callback_show(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    products = await get_user_products(user_id)

    if not products:
        await callback_query.answer("У вас нет продуктов для генерации рецептов.", show_alert=True)
        return

    await state.set_state(RecipeState.waiting_for_recipe_type)
    await callback_query.message.answer("Какой тип рецепта вы хотите?", reply_markup=kb.recipe_type_keyboard)


@router_recept.callback_query(lambda call: call.data.startswith('recipe_type_'))
async def process_recipe_type(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    recipe_type = callback_query.data.replace('recipe_type_', '')

    await state.update_data(recipe_type=recipe_type)

    products = await get_user_products(user_id)

    response = requests.post(url, headers=headers, params=params,
                             data=json.dumps(await get_recipes_from_gpt(products, recipe_type)))

    if response.status_code == 200:
        response_data = response.json()
        if 'candidates' in response_data:
            recipe_text = response_data['candidates'][0]['content']['parts'][0]['text']
            await callback_query.message.answer(recipe_text, reply_markup=kb.return_menu)
        else:
            await callback_query.message.answer("Не удалось найти рецепты с вашими продуктами.",
                                                reply_markup=kb.return_menu)
    else:
        await callback_query.message.answer("Не удалось получить рецепты.", reply_markup=kb.return_menu)
