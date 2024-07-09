from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

VOTE_BUTTON_TEXT = 'OVOZ BERISH'


def create_vote_keyboard():
    keyboard = [[KeyboardButton(text=VOTE_BUTTON_TEXT)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
