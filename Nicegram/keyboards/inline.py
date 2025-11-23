from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from locales.texts import get_text

def get_language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
    )
    return builder.as_markup()

def get_main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'instruction_btn'),
            callback_data="instruction"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'download_nicegram_btn'),
            url="https://nicegram.app/"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'check_refund_btn'),
            callback_data="check_refund"
        )
    )
    return builder.as_markup()

def get_instruction_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'back_btn'),
            callback_data="back_to_menu"
        )
    )
    return builder.as_markup()

def get_cancel_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'cancel_btn'),
            callback_data="cancel"
        )
    )
    return builder.as_markup()

def get_admin_check_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="❌ Ошибка",
            callback_data=f"admin_error_{user_id}"
        ),
        InlineKeyboardButton(
            text="✅ Успешно",
            callback_data=f"admin_success_{user_id}"
        )
    )
    return builder.as_markup()

def get_admin_panel_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'broadcast_btn'),
            callback_data="admin_broadcast"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'stats_btn'),
            callback_data="admin_stats"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'back_btn'),
            callback_data="back_to_menu"
        )
    )
    return builder.as_markup()

def get_broadcast_button_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'add_button_btn'),
            callback_data="broadcast_add_button"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'send_broadcast_btn'),
            callback_data="broadcast_send"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'cancel_btn'),
            callback_data="cancel"
        )
    )
    return builder.as_markup()

def get_broadcast_confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'confirm_broadcast_btn'),
            callback_data="broadcast_confirm"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(lang, 'cancel_btn'),
            callback_data="cancel"
        )
    )
    return builder.as_markup()

def create_broadcast_keyboard(buttons: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.row(
            InlineKeyboardButton(
                text=button['text'],
                url=button['url']
            )
        )
    return builder.as_markup()
