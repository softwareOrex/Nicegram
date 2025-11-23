import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_main_menu_keyboard, get_admin_check_keyboard
from locales.texts import get_text
from utils.database import get_user_language
from utils.states import UserStates
from config import ADMIN_ID

router = Router()
user_file_checks = {}

@router.message(UserStates.waiting_for_file, F.document)
async def process_file(message: Message, state: FSMContext, bot: Bot):
    lang = get_user_language(message.from_user.id)
    
    file_name = message.document.file_name.lower()
    if not (file_name.endswith('.txt') or file_name.endswith('.zip')):
        await message.answer(get_text(lang, 'invalid_file'))
        return
    
    data = await state.get_data()
    message_id = data.get('message_id')
    
    if message_id:
        try:
            await bot.delete_message(message.chat.id, message_id)
        except:
            pass
    
    await message.answer(get_text(lang, 'file_received'))
    
    user_info = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
    
    await bot.send_document(
        chat_id=ADMIN_ID,
        document=message.document.file_id,
        caption=get_text(lang, 'new_file_check', user=user_info, user_id=message.from_user.id),
        reply_markup=get_admin_check_keyboard(message.from_user.id),
        parse_mode="HTML"
    )
    
    user_file_checks[message.from_user.id] = {
        'lang': lang,
        'message': message
    }
    
    await state.clear()
    
    asyncio.create_task(delete_message_after_timeout(bot, message.chat.id, message.message_id, 180))

@router.message(UserStates.waiting_for_file)
async def invalid_file_type(message: Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'invalid_file'))

@router.callback_query(F.data.startswith("admin_error_"))
async def admin_error_response(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split("_")[2])
    
    user_data = user_file_checks.get(user_id)
    if not user_data:
        await callback.answer("❌ Информация о пользователе не найдена")
        return
    
    lang = user_data['lang']
    
    try:
        await bot.send_message(
            chat_id=user_id,
            text=get_text(lang, 'gift_failed')
        )
        
        await callback.message.edit_caption(
            caption=callback.message.caption + "\n\n✅ <b>Обработано: Ошибка</b>",
            parse_mode="HTML"
        )
        
        await callback.answer("✅ Пользователь уведомлен об ошибке")
    except Exception as e:
        await callback.answer(f"❌ Ошибка отправки: {str(e)}")
    
    user_file_checks.pop(user_id, None)

@router.callback_query(F.data.startswith("admin_success_"))
async def admin_success_response(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split("_")[2])
    
    user_data = user_file_checks.get(user_id)
    if not user_data:
        await callback.answer("❌ Информация о пользователе не найдена")
        return
    
    lang = user_data['lang']
    
    try:
        await bot.send_message(
            chat_id=user_id,
            text=get_text(lang, 'gift_success')
        )
        
        await callback.message.edit_caption(
            caption=callback.message.caption + "\n\n✅ <b>Обработано: Успешно</b>",
            parse_mode="HTML"
        )
        
        await callback.answer("✅ Пользователь уведомлен об успехе")
    except Exception as e:
        await callback.answer(f"❌ Ошибка отправки: {str(e)}")
    
    user_file_checks.pop(user_id, None)

async def delete_message_after_timeout(bot: Bot, chat_id: int, message_id: int, timeout: int):
    await asyncio.sleep(timeout)
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        pass
