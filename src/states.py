from aiogram.fsm.state import StatesGroup, State


class OrderMenuStates(StatesGroup):
    main_menu = State()
    product_menu = State()


class AddProduct(StatesGroup):
    product_name = State()
    quantity = State()
    quantity_unit = State()
    production_date = State()
    expiry_days = State()


class EditProduct(StatesGroup):
    choice = State()

class RecipeState(StatesGroup):
    waiting_for_recipe_type = State()
