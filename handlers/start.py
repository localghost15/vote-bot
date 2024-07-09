from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.inline import create_poll_keyboard
from keyboards.reply import create_vote_keyboard
from models.poll import Poll
from models.user import User

router = Router()
START_TEXT = "<b>Assalomu alaykum</b>.\nSo'rovnoma botga xush kelibsiz!"


@router.message(CommandStart())
async def command_start(message: Message):
    if not await User.exists(id=message.from_user.id):
        await User.create_user(message.from_user)
    text = message.text
    poll_id = text.split()[1] if len(text.split()) > 1 else None
    if poll_id:
        poll = await Poll.get_poll_by_id(poll_id=int(poll_id))
        if poll:
            options = await poll.options.all()
            await message.delete()
            await message.bot.send_chat_action(message.chat.id, 'typing')
            await message.bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,
                                           message_id=poll.message_id, reply_markup=create_poll_keyboard(options))
            return
    await message.bot.send_chat_action(message.chat.id, 'typing')
    await message.answer(START_TEXT, reply_markup=create_vote_keyboard())
