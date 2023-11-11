from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(StateFilter(None), Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Hi! I am your bot. Use /help to see available commands.")
