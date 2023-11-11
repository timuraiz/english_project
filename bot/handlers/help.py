from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(StateFilter(None), Command('help'))
async def cmd_help(message: types.Message, state: FSMContext):
    await message.answer('This is a help message. You can use /start and /process commands.')
