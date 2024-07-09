from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_poll_keyboard(options: list):
    keyboard = []
    for option in options:
        keyboard.append([InlineKeyboardButton(text=option.title, callback_data=f"vote:{option.id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_poll_draft_keyboard(options: list):
    keyboard = []
    for option in options:
        keyboard.append([InlineKeyboardButton(text=option.title, url='https://t.me/vote_bot')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_poll_list_keyboard(polls: list):
    keyboard = []
    for poll in polls:
        keyboard.append([InlineKeyboardButton(text=poll.title, callback_data=f"poll:{poll.id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
