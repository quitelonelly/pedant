from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Начать заполнение данных', callback_data='start')
        ]
    ]
)

kb_choice_result = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ ВСЕ ВЕРНО', callback_data='result'),
            InlineKeyboardButton(text='✏️ Обновить данные', callback_data='edit')
        ]
    ]
)