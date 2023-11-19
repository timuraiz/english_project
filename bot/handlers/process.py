from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.enums import ParseMode

from services.api_models import GrammarImprover, VocabularyImprover
from bot.messages import process_messages


class ProcessState(StatesGroup):
    waiting_for_text = State()
    waiting_for_approve_next_fix = State()


router = Router()


@router.message(StateFilter(None), Command('process'))
async def greetings(message: types.Message, state: FSMContext):
    await message.answer(process_messages['start'])
    await state.set_state(ProcessState.waiting_for_text)


@router.message(ProcessState.waiting_for_text)
async def process_text(message: types.Message, state: FSMContext):
    updated_text, number_of_improvements = await GrammarImprover(text=message.text).process()
    await state.update_data(text=message.text)
    await message.answer(
        process_messages['improved_text'].format(
            number=number_of_improvements, updated_text=updated_text
        ), parse_mode=ParseMode.HTML
    )
    await message.answer(process_messages['request_approve'])
    await state.set_state(ProcessState.waiting_for_approve_next_fix)


@router.message(ProcessState.waiting_for_approve_next_fix, F.text.lower() == 'no')
async def finish_process_no(message: types.Message, state: FSMContext):
    await message.answer(process_messages['no'])
    await state.clear()


@router.message(ProcessState.waiting_for_approve_next_fix, F.text.lower() == 'yes')
async def finish_proces_yes(message: types.Message, state: FSMContext):
    stored_data = await state.get_data()
    text = stored_data.get('text', None)
    updated_text, number_of_improvements = await VocabularyImprover(text=text).process()
    await message.answer(
        process_messages['improved_text'].format(
            number=number_of_improvements, updated_text=updated_text
        ), parse_mode=ParseMode.HTML
    )
    await state.clear()
