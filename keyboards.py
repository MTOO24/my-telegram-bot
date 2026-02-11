from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                          InlineKeyboardMarkup, InlineKeyboardButton)
from config import config

# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 КАТАЛОГ УСЛУГ"), 
             KeyboardButton(text="🛠 ДОРАБОТКА БОТА")],
            [KeyboardButton(text="❓ ЧАСТЫЕ ВОПРОСЫ"), 
             KeyboardButton(text="📂 ПОРТФОЛИО")],
            [KeyboardButton(text="👨‍💼 СВЯЗАТЬСЯ С МЕНЕДЖЕРОМ")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел ↓"
    )
    return keyboard

# ===== КАТАЛОГ УСЛУГ =====
def catalog_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎯 БАЗОВЫЙ БОТ (от 500₽)", callback_data="catalog_basic")],
            [InlineKeyboardButton(text="🚀 БИЗНЕС-БОТ (от 2 000₽)", callback_data="catalog_business")],
            [InlineKeyboardButton(text="🧠 СЛОЖНЫЙ БОТ (от 7 000₽)", callback_data="catalog_complex")],
            [InlineKeyboardButton(text="↩️ В ГЛАВНОЕ МЕНЮ", callback_data="main_menu")]
        ]
    )
    return keyboard

# ===== КНОПКИ ДЛЯ КАТАЛОГА =====
def catalog_item_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Обсудить проект", 
                                 url=f"https://t.me/{config.MANAGER_USERNAME}")],
            [InlineKeyboardButton(text="↩️ В каталог", callback_data="catalog")]
        ]
    )
    return keyboard

# ===== КЛАВИАТУРА ДОРАБОТКИ =====
def fix_bot_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Обсудить доработку", 
                                 url=f"https://t.me/{config.MANAGER_USERNAME}")],
            [InlineKeyboardButton(text="↩️ В ГЛАВНОЕ МЕНЮ", callback_data="main_menu")]
        ]
    )
    return keyboard

# ===== FAQ КЛАВИАТУРА =====
def faq_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1️⃣ Как происходит процесс разработки?", callback_data="faq_1")],
            [InlineKeyboardButton(text="2️⃣ Что нужно подготовить перед заказом?", callback_data="faq_2")],
            [InlineKeyboardButton(text="3️⃣ Поддерживаете бота после запуска?", callback_data="faq_3")],
            [InlineKeyboardButton(text="4️⃣ На каких платформах делаете ботов?", callback_data="faq_4")],
            [InlineKeyboardButton(text="↩️ В ГЛАВНОЕ МЕНЮ", callback_data="main_menu")]
        ]
    )
    return keyboard

# ===== ПОРТФОЛИО КЛАВИАТУРА =====
def portfolio_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🦷 Кейс: Стоматология", callback_data="case_1")],
            [InlineKeyboardButton(text="🛒 Кейс: Мини-маркет", callback_data="case_2")],
            [InlineKeyboardButton(text="⚖️ Кейс: Юридическая фирма", callback_data="case_3")],
            [InlineKeyboardButton(text="↩️ В ГЛАВНОЕ МЕНЮ", callback_data="main_menu")]
        ]
    )
    return keyboard

# ===== КНОПКА СВЯЗИ С МЕНЕДЖЕРОМ =====
def manager_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👨‍💼 Написать менеджеру", 
                                 url=f"https://t.me/{config.MANAGER_USERNAME}")],
            [InlineKeyboardButton(text="↩️ В ГЛАВНОЕ МЕНЮ", callback_data="main_menu")]
        ]
    )
    return keyboard

# ===== КНОПКА НАЗАД В FAQ =====
def back_to_faq_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="↩️ К вопросам", callback_data="faq")]
        ]
    )
    return keyboard

# ===== КНОПКА НАЗАД В ПОРТФОЛИО =====
def back_to_portfolio_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="↩️ К кейсам", callback_data="portfolio")]
        ]
    )
    return keyboard