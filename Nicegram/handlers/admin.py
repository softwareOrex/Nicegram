import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from utils.database import (
    get_user_language, get_users_count, get_all_users,
    get_broadcast_stats, update_broadcast_stats, add_user
)
from utils.states import AdminStates
from locales.texts import get_text
from keyboards.inline import (
    get_admin_panel_keyboard, get_broadcast_button_keyboard,
    get_broadcast_confirm_keyboard, create_broadcast_keyboard,
    get_cancel_keyboard
)

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

@router.message(Command("admin"))
async def admin_panel(message: Message):

    if not is_admin(message.from_user.id):
        return
    
    add_user(message.from_user.id)
    lang = get_user_language(message.from_user.id)
    stats = get_broadcast_stats()
    
    text = get_text(
        lang, 'admin_panel',
        users_count=get_users_count(),
        total_sent=stats['total_sent'],
        total_failed=stats['total_failed'],
        last_broadcast=stats['last_broadcast'] or 'Нет данных' if lang == 'ru' else 'No data'
    )
    
    await message.answer(
        text,
        reply_markup=get_admin_panel_keyboard(lang)
    )

@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):

    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен" if get_user_language(callback.from_user.id) == 'ru' else "Access denied", show_alert=True)
        return
    
    lang = get_user_language(callback.from_user.id)
    stats = get_broadcast_stats()
    
    text = get_text(
        lang, 'admin_panel',
        users_count=get_users_count(),
        total_sent=stats['total_sent'],
        total_failed=stats['total_failed'],
        last_broadcast=stats['last_broadcast'] or 'Нет данных' if lang == 'ru' else 'No data'
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_admin_panel_keyboard(lang)
    )
    await callback.answer()

@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: CallbackQuery, state: FSMContext):

    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен" if get_user_language(callback.from_user.id) == 'ru' else "Access denied", show_alert=True)
        return
    
    lang = get_user_language(callback.from_user.id)
    
    await callback.message.edit_text(
        get_text(lang, 'broadcast_start'),
        reply_markup=get_cancel_keyboard(lang)
    )
    await state.set_state(AdminStates.waiting_for_broadcast_text)
    await callback.answer()

@router.message(AdminStates.waiting_for_broadcast_text)
async def receive_broadcast_text(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return
    
    lang = get_user_language(message.from_user.id)
    
    await state.update_data(broadcast_text=message.text, buttons=[])
    
    await message.answer(
        get_text(lang, 'broadcast_add_button'),
        reply_markup=get_broadcast_button_keyboard(lang)
    )

@router.callback_query(F.data == "broadcast_add_button")
async def add_button_prompt(callback: CallbackQuery, state: FSMContext):

    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен" if get_user_language(callback.from_user.id) == 'ru' else "Access denied", show_alert=True)
        return
    
    lang = get_user_language(callback.from_user.id)
    
    await callback.message.edit_text(
        get_text(lang, 'button_text_prompt'),
        reply_markup=get_cancel_keyboard(lang)
    )
    await state.set_state(AdminStates.waiting_for_button_text)
    await callback.answer()

@router.message(AdminStates.waiting_for_button_text)
async def receive_button_text(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return
    
    lang = get_user_language(message.from_user.id)
    
    await state.update_data(button_text=message.text)
    
    await message.answer(
        get_text(lang, 'button_url_prompt'),
        reply_markup=get_cancel_keyboard(lang)
    )
    await state.set_state(AdminStates.waiting_for_button_url)

@router.message(AdminStates.waiting_for_button_url)
async def receive_button_url(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return
    
    lang = get_user_language(message.from_user.id)
    
    if not message.text.startswith(('http://', 'https://')):
        await message.answer(get_text(lang, 'invalid_url'))
        return
    
    data = await state.get_data()
    button_text = data.get('button_text')
    buttons = data.get('buttons', [])
    
    buttons.append({'text': button_text, 'url': message.text})
    await state.update_data(buttons=buttons)
    
    await message.answer(
        get_text(lang, 'button_added', text=button_text, url=message.text)
    )
    
    await message.answer(
        get_text(lang, 'broadcast_add_button'),
        reply_markup=get_broadcast_button_keyboard(lang)
    )

@router.callback_query(F.data == "broadcast_send")
async def preview_broadcast(callback: CallbackQuery, state: FSMContext):

    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен" if get_user_language(callback.from_user.id) == 'ru' else "Access denied", show_alert=True)
        return
    
    lang = get_user_language(callback.from_user.id)
    data = await state.get_data()
    
    broadcast_text = data.get('broadcast_text', '')
    buttons = data.get('buttons', [])
    
    preview_text = get_text(
        lang, 'broadcast_preview',
        text=broadcast_text,
        users_count=get_users_count(),
        buttons_count=len(buttons)
    )
    
    if buttons:
        keyboard = create_broadcast_keyboard(buttons)
        await callback.message.edit_text(broadcast_text, reply_markup=keyboard)
        await callback.message.answer(
            preview_text,
            reply_markup=get_broadcast_confirm_keyboard(lang)
        )
    else:
        await callback.message.edit_text(
            preview_text,
            reply_markup=get_broadcast_confirm_keyboard(lang)
        )
    
    await callback.answer()

@router.callback_query(F.data == "broadcast_confirm")
async def confirm_broadcast(callback: CallbackQuery, state: FSMContext):

    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен" if get_user_language(callback.from_user.id) == 'ru' else "Access denied", show_alert=True)
        return
    
    lang = get_user_language(callback.from_user.id)
    data = await state.get_data()
    
    broadcast_text = data.get('broadcast_text', '')
    buttons = data.get('buttons', [])
    
    await callback.message.edit_text(get_text(lang, 'broadcasting'))
    await callback.answer()
    
    users = get_all_users()
    sent = 0
    failed = 0
    
    keyboard = create_broadcast_keyboard(buttons) if buttons else None
    
    for user_id in users:
        try:
            if keyboard:
                await callback.bot.send_message(
                    user_id,
                    broadcast_text,
                    reply_markup=keyboard
                )
            else:
                await callback.bot.send_message(user_id, broadcast_text)
            sent += 1
            await asyncio.sleep(0.05)  
        except Exception:
            failed += 1
    
    update_broadcast_stats(sent, failed)
    
    result_text = get_text(
        lang, 'broadcast_complete',
        sent=sent,
        failed=failed,
        total=len(users)
    )
    
    await callback.message.answer(
        result_text,
        reply_markup=get_admin_panel_keyboard(lang)
    )
    
    await state.clear()
