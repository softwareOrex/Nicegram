from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from pathlib import Path

from keyboards.inline import get_main_menu_keyboard, get_instruction_keyboard, get_cancel_keyboard
from locales.texts import get_text
from utils.database import get_user_language
from utils.states import UserStates
from config import MAIN_MENU_PHOTO, INSTRUCTION_PHOTO

router = Router()

@router.callback_query(F.data == "instruction")
async def show_instruction(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    
    instruction_photo_path = Path(INSTRUCTION_PHOTO)
    
    if callback.message.photo and instruction_photo_path.exists():
        photo = FSInputFile(instruction_photo_path)
        try:
            await callback.message.edit_media(
                media=photo,
            )
        except:
            pass
    
    await callback.message.caption(
        caption=get_text(lang, 'instruction_text'),
        reply_markup=get_instruction_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    
    await state.clear()
    
    await callback.message.edit_caption(
        caption=get_text(lang, 'welcome'),
        reply_markup=get_main_menu_keyboard(lang)
    )
    await callback.answer()

@router.callback_query(F.data == "check_refund")
async def start_check_refund(callback: CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    
    await callback.message.delete()
    
    msg = await callback.message.answer(
        get_text(lang, 'send_file'),
        reply_markup=get_cancel_keyboard(lang)
    )
    
    await state.set_state(UserStates.waiting_for_file)
    
    await state.update_data(message_id=msg.message_id)
    
    await callback.answer()

@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    
    await state.clear()
    
    await callback.message.delete()
    
    photo_path = Path(MAIN_MENU_PHOTO)
    
    if photo_path.exists() and photo_path.is_file():
        photo = FSInputFile(photo_path)
        await callback.message.answer_photo(
            photo=photo,
            caption=get_text(lang, 'welcome'),
            reply_markup=get_main_menu_keyboard(lang)
        )
    else:
        await callback.message.answer(
            f"🛡️ {get_text(lang, 'welcome')}",
            reply_markup=get_main_menu_keyboard(lang)
        )
    
    await callback.answer(get_text(lang, 'cancelled'))
