from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)


markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить продукты", callback_data="add_products")
    ],
    [
        InlineKeyboardButton(text="Посмотреть продукты", callback_data="view_products")
    ],
    [
        InlineKeyboardButton(text="Показать рецепты", callback_data="show_recipes")
    ]
])

add_product = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить продукты вручную", callback_data="manually")
    ],
    [
        InlineKeyboardButton(text="Сканировать чек", callback_data="automatically")
    ]
])

replay_product = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить ещё один продукт", callback_data="manually")
    ],
    [
        InlineKeyboardButton(text="Вернуться в меню", callback_data="menu")
    ]
])

product_edit = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Название", callback_data="edit_name"),
            InlineKeyboardButton(text="Количество", callback_data="edit_quantity"),
        ],
        [
            InlineKeyboardButton(text="Объем", callback_data="edit_volume"),
            InlineKeyboardButton(text="Дата производства", callback_data="edit_production_date"),
            InlineKeyboardButton(text="Срок годности", callback_data="edit_expiry_date"),
        ],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel_edit")]
    ]
)

recipe_type_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Завтрак", callback_data="recipe_type_breakfast")],
        [InlineKeyboardButton(text="Первое", callback_data="recipe_type_first")],
        [InlineKeyboardButton(text="Второе", callback_data="recipe_type_second")],
        [InlineKeyboardButton(text="Десерт", callback_data="recipe_type_dessert")],
        [InlineKeyboardButton(text="Любое", callback_data="recipe_type_any")],
    ]
)

recipe_type_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Завтрак", callback_data="recipe_type_breakfast")],
        [InlineKeyboardButton(text="Первое", callback_data="recipe_type_first")],
        [InlineKeyboardButton(text="Второе", callback_data="recipe_type_second")],
        [InlineKeyboardButton(text="Десерт", callback_data="recipe_type_dessert")],
        [InlineKeyboardButton(text="Любое", callback_data="recipe_type_any")],
    ]
)

return_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в меню", callback_data="menu")]
    ]
)
