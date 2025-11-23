from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from pathlib import Path

from keyboards.inline import get_language_keyboard, get_main_menu_keyboard
from locales.texts import get_text
from utils.database import set_user_language, get_user_language, add_user
from config import MAIN_MENU_PHOTO

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):

    await state.clear()
    
    add_user(message.from_user.id)

    user_lang = get_user_language(message.from_user.id)
    
    if user_lang:
        await show_main_menu(message, user_lang)
    else:
        await message.answer(
            get_text('ru', 'choose_language'),
            reply_markup=get_language_keyboard(),
            parse_mode='HTML'
        )

@router.callback_query(F.data.startswith("lang_"))
async def process_language_selection(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    set_user_language(user_id, lang)
    
    await callback.message.delete()
    
    await show_main_menu(callback.message, lang)
    await callback.answer()

async def show_main_menu(message: Message, lang: str):
    photo_path = Path(MAIN_MENU_PHOTO)
    
    if photo_path.exists() and photo_path.is_file():
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo,
            caption=get_text(lang, 'welcome'),
            reply_markup=get_main_menu_keyboard(lang)
        )
    else:
        await message.answer(
            f"🛡️ {get_text(lang, 'welcome')}",
            reply_markup=get_main_menu_keyboard(lang)
        )
