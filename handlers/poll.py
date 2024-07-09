from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline import create_poll_list_keyboard, create_poll_keyboard
from keyboards.reply import VOTE_BUTTON_TEXT
from models.poll import Poll, PollOption
from models.vote import Vote
from states.poll import PollCreation

router = Router()

ENTER_TITLE_TEXT = "So'rovnoma sarlavhasini kiriting"
ENTER_POST_TEXT = "So'rovnoma matnini kiriting"
ENTER_OPTIONS_TEXT = "Ovoz berish uchun so'rovnomani variantlarini yozing"
CHOOSE_POLL_TEXT = "Quyida ko'rsatilgan so'rovnomalardan birini tanlang 👇"
ALREADY_VOTED_TEXT = "❗Sizning ovozingiz qabul qilinmadi. Siz ushbu so'rovnomaga ovoz bergansiz."
VOTED_TEXT = "✅ Sizning {}ga bergan ovozingiz muvaffaqiyatli qabul qilindi!"


@router.message(Command("poll"))
async def command_poll(message: Message, state: FSMContext):
    await message.bot.send_chat_action(message.chat.id, 'typing')
    await message.answer(ENTER_TITLE_TEXT)
    await state.set_state(PollCreation.title)


@router.message(PollCreation.title)
async def poll_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.bot.send_chat_action(message.chat.id, 'typing')
    await message.answer(ENTER_POST_TEXT)
    await state.set_state(PollCreation.post)


@router.message(PollCreation.post)
async def poll_title(message: Message, state: FSMContext):
    await state.update_data(post_message_id=message.message_id)
    await message.bot.send_chat_action(message.chat.id, 'typing')
    await message.answer(ENTER_OPTIONS_TEXT)
    await state.set_state(PollCreation.options)


@router.message(PollCreation.options)
async def poll_title(message: Message, state: FSMContext):
    options = message.text.split()
    data = await state.get_data()
    poll = await Poll.create_poll(title=data['title'], message_id=data['post_message_id'])
    for option in options:
        await PollOption.create_poll_option(option, poll)
    await message.bot.send_chat_action(message.chat.id, 'typing')
    await message.bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,
                                   message_id=data['post_message_id'])
    await state.clear()


@router.message(lambda message: message.text == VOTE_BUTTON_TEXT)
async def vote(message: Message):
    polls = await Poll.get_all_polls()
    await message.bot.send_chat_action(message.chat.id, 'typing')
    await message.answer(CHOOSE_POLL_TEXT, reply_markup=create_poll_list_keyboard(polls))


@router.callback_query(lambda query: query.data.startswith("poll:"))
async def choose_poll(query: CallbackQuery):
    poll_id = int(query.data.split(":")[1])
    poll = await Poll.get_poll_by_id(poll_id)
    options = await poll.options.all()
    await query.message.delete()
    await query.message.bot.send_chat_action(query.message.chat.id, 'typing')
    await query.bot.copy_message(chat_id=query.message.chat.id, from_chat_id=query.message.chat.id,
                                 message_id=poll.message_id, reply_markup=create_poll_keyboard(options))


@router.callback_query(lambda query: query.data.startswith("vote:"))
async def choose_vote(query: CallbackQuery):
    option_id = int(query.data.split(":")[1])
    poll_option = await PollOption.get(id=option_id)
    poll = await poll_option.poll
    voted = await Vote.vote_exists(query.from_user.id, poll.id)
    await query.message.delete()
    await query.message.bot.send_chat_action(query.message.chat.id, 'typing')
    if voted:
        await query.message.answer(ALREADY_VOTED_TEXT)
        return
    await Vote.create(user_id=query.from_user.id, poll_id=poll.id)
    await query.message.answer(VOTED_TEXT.format(poll_option.title))
