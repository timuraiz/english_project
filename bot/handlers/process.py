from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.enums import ParseMode

from ai21.services.api_models import GrammarImprover, VocabularyImprover


class ProcessState(StatesGroup):
    waiting_for_text = State()
    waiting_for_approve_next_fix = State()


router = Router()


@router.message(StateFilter(None), Command('process'))
async def greetings(message: types.Message, state: FSMContext):
    await message.answer('Send me text on any topic and I will try to evaluate it!')
    await state.set_state(ProcessState.waiting_for_text)


@router.message(ProcessState.waiting_for_text)
async def process_text(message: types.Message, state: FSMContext):
    await message.answer('Here is the corrected version:')
    updated_text, number_of_improvements = await GrammarImprover(text=message.text).process()
    await state.update_data(text=message.text)
    await message.answer(f'Number of improvements: <b>{number_of_improvements}</b>', parse_mode=ParseMode.HTML)
    await message.answer(updated_text, parse_mode=ParseMode.HTML)
    await message.answer('Do you want to see next improvements?(yes or no)')
    await state.set_state(ProcessState.waiting_for_approve_next_fix)


@router.message(ProcessState.waiting_for_approve_next_fix, F.text.lower() == 'no')
async def finish_process_no(message: types.Message, state: FSMContext):
    await message.answer('Okay. See you!')
    await state.clear()


@router.message(ProcessState.waiting_for_approve_next_fix, F.text.lower() == 'yes')
async def finish_proces_yes(message: types.Message, state: FSMContext):
    await message.answer('Okay, I get you:). Here is the corrected version:')
    stored_data = await state.get_data()
    text = stored_data.get('text', None)
    if text is None:
        await message.answer('I lost your text:(')
    else:
        updated_text, number_of_improvements = await VocabularyImprover(text=text).process()
        await message.answer(f'Number of improvements: <b>{number_of_improvements}</b>', parse_mode=ParseMode.HTML)
        await message.answer(updated_text, parse_mode=ParseMode.HTML)
    await state.clear()
