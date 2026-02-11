import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import config
import keyboards

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Валидация конфигурации перед запуском
try:
    config.config.validate()
    logger.info("✅ Конфигурация проверена успешно")
    
    # Инициализация бота
    bot = Bot(token=config.config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
except ValueError as e:
    logger.error(str(e))
    logger.error("📝 Создайте файл .env в папке проекта со следующим содержимым:")
    logger.error("BOT_TOKEN=ваш_токен_бота_от_BotFather")
    logger.error("MANAGER_USERNAME=zamjk")
    logger.error("ADMIN_ID=8366233854")
    exit(1)
except Exception as e:
    logger.error(f"❌ Ошибка инициализации бота: {e}")
    exit(1)

# Словарь для хранения последних сообщений пользователей
user_last_messages = {}

# ===== ФУНКЦИИ ДЛЯ УПРАВЛЕНИЯ СООБЩЕНИЯМИ =====

async def delete_previous_messages(user_id: int):
    """Удаляет предыдущие сообщения бота у пользователя"""
    if user_id in user_last_messages:
        for message_id in user_last_messages[user_id]:
            try:
                await bot.delete_message(chat_id=user_id, message_id=message_id)
            except:
                pass
        user_last_messages[user_id] = []

async def save_message_id(user_id: int, message_id: int):
    """Сохраняет ID сообщения для последующего удаления"""
    if user_id not in user_last_messages:
        user_last_messages[user_id] = []
    user_last_messages[user_id].append(message_id)

async def send_and_save_message(user_id: int, text: str, reply_markup=None):
    """Отправляет сообщение и сохраняет его ID"""
    await delete_previous_messages(user_id)
    message = await bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=reply_markup
    )
    await save_message_id(user_id, message.message_id)
    return message

async def send_photo_with_caption(user_id: int, photo_path: str, caption: str, reply_markup=None):
    """Отправляет фото с подписью"""
    await delete_previous_messages(user_id)
    try:
        with open(photo_path, "rb") as photo_file:
            photo_bytes = photo_file.read()
            photo_input = types.BufferedInputFile(
                photo_bytes,
                filename="botmaster_photo.jpg"
            )
            
            message = await bot.send_photo(
                chat_id=user_id,
                photo=photo_input,
                caption=caption,
                reply_markup=reply_markup
            )
    except FileNotFoundError:
        logger.warning(f"Файл {photo_path} не найден! Отправляю текст без фото.")
        message = await bot.send_message(
            chat_id=user_id,
            text=caption,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке фото: {e}")
        message = await bot.send_message(
            chat_id=user_id,
            text=caption,
            reply_markup=reply_markup
        )
    
    await save_message_id(user_id, message.message_id)
    return message

# ===== ТЕКСТЫ СООБЩЕНИЙ =====

WELCOME_TEXT = """👋 Привет! Я — виртуальный помощник студии <b>«БотМастер.РФ»</b>.

Мы создаем умных Telegram-ботов, которые:
• 🕒 <i>Экономят до 70% времени</i> на рутине
• 💰 <i>Приносят заявки и продажи</i> 24/7
• 📈 <i>Автоматизируют</i> обслуживание клиентов

Выберите раздел, который вас интересует ⤵️"""

CATALOG_TEXT = """<b>Выберите тип бота, который соответствует вашим задачам:</b>

Каждый проект мы дорабатываем индивидуально под ваш бизнес."""

FIX_BOT_TEXT = """🔧 <b>ДОРАБОТКА И ИСПРАВЛЕНИЕ БОТОВ</b>

У вас уже есть бот, но:
• Нужно добавить новую функцию?
• Появились ошибки после обновления?
• Хотите улучшить существующий функционал?
• Нужно интегрировать с новой системой?

<b>Мы поможем!</b>

<i>Что мы делаем:</i>
✅ Исправляем ошибки и баги в существующих ботах
✅ Добавляем новые функции и кнопки
✅ Интегрируем с внешними API и сервисами
✅ Оптимизируем код для быстрой работы
✅ Переносим ботов на новые версии библиотек
✅ Настраиваем вебхуки и серверную часть

<i>Примеры задач:</i>
• Добавить оплату картой в бот-магазин
• Интегрировать с CRM системой (AmoCRM, Bitrix24)
• Исправить ошибки в работе с базой данных
• Добавить рассылку для клиентов
• Настроить аналитику и сбор статистики

<b>💰 Стоимость:</b> от 300 рублей (зависит от сложности задачи)
<b>⏱ Сроки:</b> от нескольких часов до 3 дней

<i>Присылайте вашего бота и описание задачи — оценим быстро и бесплатно!</i>"""

BASIC_BOT_TEXT = """🎯 <b>БАЗОВЫЙ БОТ — ваш цифровой ассистент</b>

<i>Идеально для:</i> старта автоматизации, презентации услуг, разгрузки поддержки.

<i>Примеры:</i>
• Бот-визитка для компании или специалиста
• Простой бот техподдержки с ответами на FAQ
• Бот-опросник для сбора отзывов и контактов
• Информационный бот для мероприятия

<b>📌 Базовый функционал:</b>
✅ Многоуровневое меню (до 5 основных кнопок)
✅ Текстовые ответы по базе знаний (Q&A)
✅ Сбор контактов (имя, телефон, email)
✅ Пересылка заявок в чат менеджера
✅ Интеграция с Google Таблицами для сбора данных

<b>⏱ Срок разработки:</b> 1-5 рабочих дней
<b>💰 Стоимость:</b> от 500 рублей

<i>Заинтересовало? Узнайте подробности!</i>"""

BUSINESS_BOT_TEXT = """🚀 <b>БИЗНЕС-БОТ — автомат для продаж и сервиса</b>

<i>Идеально для:</i> интернет-магазинов, сервисных компаний, образовательных проектов.

<i>Примеры:</i>
• Бот с каталогом товаров и корзиной
• Бот для записи на услуги (салоны, врачи)
• Бот-лояльности с картой клиента
• Образовательный бот с доступом к урокам

<b>📌 Расширенный функционал:</b>
✅ Сложное интерактивное меню
✅ Система корзины и оформления заказа
✅ Интеграция с Google Таблицами/Календарем
✅ Мини-CRM внутри бота
✅ Отправка документов, PDF, медиафайлов
✅ Автоматические напоминания

<b>⏱ Срок разработки:</b> 2-6 рабочих дней
<b>💰 Стоимость:</b> от 2 000 рублей

<i>Хотите такой же результат?</i>"""

COMPLEX_BOT_TEXT = """🧠 <b>СЛОЖНЫЙ БОТ — инновационное решение для масштаба</b>

<i>Идеально для:</i> интеграций с внешними системами, AI-решений, сложных бизнес-процессов.

<i>Примеры:</i>
• Бот с ИИ (GPT/Claude) для интеллектуальной поддержки
• Бот как часть внутренней CRM-системы
• Бот со сложными воронками и триггерными рассылками
• Бот с онлайн-оплатой и личными кабинетами

<b>📌 Максимальный функционал:</b>
✅ Интеграция ChatGPT/Claude API
✅ Работа со сторонними API (1C, Битрикс24, AmoCRM)
✅ Система личных кабинетов пользователей
✅ Интеграция платежных систем (ЮKassa и др.)
✅ Сложная аналитика и дашборды
✅ Кастомизация под уникальные процессы

<b>⏱ Срок разработки:</b> 3-12 рабочих дней
<b>💰 Стоимость:</b> от 7 000 рублей

<i>Есть сложная задача? Решим её!</i>"""

FAQ_TEXT = """<b>Часто задаваемые вопросы</b>

Выберите вопрос, чтобы увидеть ответ:"""

FAQ_ANSWERS = {
    "faq_1": """🔧 <b>Процесс разработки:</b>

1. <i>Бесплатная консультация</i> — обсуждение задач и возможностей
2. <i>Техническое задание</i> — детальный план с согласованием
3. <i>Дизайн и прототип</i> — интерфейс и логика диалогов
4. <i>Разработка и тестирование</i> — программирование и проверка
5. <i>Запуск и обучение</i> — передача бота и инструктаж

На каждом этапе вы вносите правки. Все прозрачно!""",
    
    "faq_2": """📋 <b>Что подготовить:</b>

• <i>Цель бота</i> — какую проблему решаем?
• <i>Контент</i> — тексты, описание услуг, ответы на вопросы
• <i>Материалы</i> — логотип, фирменные цвета, ссылки
• <i>Интеграции</i> — доступы к сервисам (если нужны)

Не переживайте, если чего-то нет — поможем подготовить!""",
    
    "faq_3": """🛠 <b>Поддержка после запуска:</b>

Да, мы предлагаем три варианта:

• <i>Базовый</i> — гарантийная поддержка 1 месяц
• <i>Стандарт</i> — обновление контента + техподдержка (от 3 000₽/мес)
• <i>VIP</i> — полное ведение и развитие бота (от 10 000₽/мес)

Без вашего согласия бот никогда не останется без внимания.""",
    
    "faq_4": """🌐 <b>Платформы:</b>

• <i>Telegram</i> — наша основная специализация
• <i>ВКонтакте</i> — для сообществ и молодой аудитории
• <i>Веб-виджеты</i> — для встраивания на сайт
• <i>WhatsApp Business API</i> — для крупных проектов

<b>Telegram</b> — самый гибкий и популярный вариант в РФ/СНГ."""
}

PORTFOLIO_TEXT = """<b>Наши кейсы</b>

Реальные примеры ботов, которые уже работают и приносят результат:"""

PORTFOLIO_CASES = {
    "case_1": """🦷 <b>Стоматология "Улыбка" (Базовый бот)</b>

<b>Задача:</b> Разгрузить администраторов от однотипных вопросов про график, цены и запись.

<b>Решение:</b> 
• Бот с онлайн-записью к конкретному врачу
• Автоответы по ценам на услуги
• Напоминания о визите за 24 часа

<b>Результат:</b>
✅ 40% звонков перешли на бота
✅ Администраторы сосредоточились на клиентах в клинике
✅ Сократилось количество опозданий""",
    
    "case_2": """🛒 <b>Мини-маркет "У дома" (Бизнес-бот)</b>

<b>Задача:</b> Автоматизировать прием заказов без найма оператора.

<b>Решение:</b>
• Каталог с фото товаров и актуальными ценами
• Корзина и выбор времени доставки
• Интеграция заказов в Google Таблицу для сборщиков

<b>Результат:</b>
✅ 37% всех заказов за 2 месяца через бота
✅ Средний чек вырос на 15%
✅ Время обработки заказа сократилось в 3 раза""",
    
    "case_3": """⚖️ <b>Юридическая фирма "Право" (Сложный бот)</b>

<b>Задача:</b> Ускорить поиск документов и подготовку черновиков.

<b>Решение:</b>
• Интеграция GPT-4 для поиска по базе документов
• Генерация черновиков договоров по запросу
• Личные кабинеты сотрудников с историей

<b>Результат:</b>
✅ Время на подготовку документов сократилось в 3 раза
✅ Бот стал основным рабочим инструментом
✅ Повысилась точность поиска прецедентов"""
}

MANAGER_TEXT = f"""✨ <b>Отлично! Вы на правильном пути к автоматизации.</b>

Чтобы обсудить ваш проект, получить индивидуальный расчет или задать вопросы — напишите напрямую нашему менеджеру.

<b>Что будет дальше:</b>
1. Вы расскажете о своей задаче
2. Мы зададим уточняющие вопросы
3. Подготовим варианты решения и расчет
4. Зафиксируем сроки и приступим к работе

<i>Менеджер ответит в течение 15 минут в рабочее время (Пн-Пт, 10:00-19:00 по МСК).</i>"""

# ===== ОБРАБОТЧИКИ КОМАНД =====

@dp.message(Command("start", "menu"))
async def cmd_start(message: types.Message):
    """Обработчик команд /start и /menu - отправляет фото с приветствием"""
    await send_photo_with_caption(
        user_id=message.from_user.id,
        photo_path="photo.jpg",
        caption=WELCOME_TEXT,
        reply_markup=keyboards.main_menu()
    )

@dp.message(F.text == "📋 КАТАЛОГ УСЛУГ")
async def catalog_handler(message: types.Message):
    await send_and_save_message(
        user_id=message.from_user.id,
        text=CATALOG_TEXT,
        reply_markup=keyboards.catalog_keyboard()
    )

@dp.message(F.text == "🛠 ДОРАБОТКА БОТА")
async def fix_bot_handler(message: types.Message):
    await send_and_save_message(
        user_id=message.from_user.id,
        text=FIX_BOT_TEXT,
        reply_markup=keyboards.fix_bot_keyboard()
    )

@dp.message(F.text == "❓ ЧАСТЫЕ ВОПРОСЫ")
async def faq_handler(message: types.Message):
    await send_and_save_message(
        user_id=message.from_user.id,
        text=FAQ_TEXT,
        reply_markup=keyboards.faq_keyboard()
    )

@dp.message(F.text == "📂 ПОРТФОЛИО")
async def portfolio_handler(message: types.Message):
    await send_and_save_message(
        user_id=message.from_user.id,
        text=PORTFOLIO_TEXT,
        reply_markup=keyboards.portfolio_keyboard()
    )

@dp.message(F.text == "👨‍💼 СВЯЗАТЬСЯ С МЕНЕДЖЕРОМ")
async def manager_handler(message: types.Message):
    await send_and_save_message(
        user_id=message.from_user.id,
        text=MANAGER_TEXT,
        reply_markup=keyboards.manager_keyboard()
    )

# ===== ОБРАБОТЧИКИ CALLBACK-ЗАПРОСОВ =====

@dp.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: types.CallbackQuery):
    """Кнопка 'В главное меню' - отправляет фото"""
    await send_photo_with_caption(
        user_id=callback.from_user.id,
        photo_path="photo.jpg",
        caption=WELCOME_TEXT,
        reply_markup=keyboards.main_menu()
    )
    
    try:
        await callback.message.delete()
    except:
        pass
    await callback.answer()

@dp.callback_query(F.data == "catalog")
async def catalog_callback(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(CATALOG_TEXT, reply_markup=keyboards.catalog_keyboard())
    except:
        await send_and_save_message(
            user_id=callback.from_user.id,
            text=CATALOG_TEXT,
            reply_markup=keyboards.catalog_keyboard()
        )
    await callback.answer()

@dp.callback_query(F.data == "catalog_basic")
async def basic_bot_callback(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(BASIC_BOT_TEXT, reply_markup=keyboards.catalog_item_keyboard())
    except:
        await send_and_save_message(
            user_id=callback.from_user.id,
            text=BASIC_BOT_TEXT,
            reply_markup=keyboards.catalog_item_keyboard()
        )
    await callback.answer()

@dp.callback_query(F.data == "catalog_business")
async def business_bot_callback(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(BUSINESS_BOT_TEXT, reply_markup=keyboards.catalog_item_keyboard())
    except:
        await send_and_save_message(
            user_id=callback.from_user.id,
            text=BUSINESS_BOT_TEXT,
            reply_markup=keyboards.catalog_item_keyboard()
        )
    await callback.answer()

@dp.callback_query(F.data == "catalog_complex")
async def complex_bot_callback(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(COMPLEX_BOT_TEXT, reply_markup=keyboards.catalog_item_keyboard())
    except:
        await send_and_save_message(
            user_id=callback.from_user.id,
            text=COMPLEX_BOT_TEXT,
            reply_markup=keyboards.catalog_item_keyboard()
        )
    await callback.answer()

@dp.callback_query(F.data == "faq")
async def faq_callback(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(FAQ_TEXT, reply_markup=keyboards.faq_keyboard())
    except:
        await send_and_save_message(
            user_id=callback.from_user.id,
            text=FAQ_TEXT,
            reply_markup=keyboards.faq_keyboard()
        )
    await callback.answer()

@dp.callback_query(F.data.startswith("faq_"))
async def faq_answer_callback(callback: types.CallbackQuery):
    answer_text = FAQ_ANSWERS.get(callback.data, "Ответ не найден")
    try:
        await callback.message.edit_text(answer_text, reply_markup=keyboards.back_to_faq_keyboard())
    except:
        await send_and_save_message(
            user_id=callback.from_user.id,
            text=answer_text,
            reply_markup=keyboards.back_to_faq_keyboard()
        )
    await callback.answer()

@dp.callback_query(F.data == "portfolio")
async def portfolio_callback(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(PORTFOLIO_TEXT, reply_markup=keyboards.portfolio_keyboard())
    except:
        await send_and_save_message(
            user_id=callback.from_user.id,
            text=PORTFOLIO_TEXT,
            reply_markup=keyboards.portfolio_keyboard()
        )
    await callback.answer()

@dp.callback_query(F.data.startswith("case_"))
async def portfolio_case_callback(callback: types.CallbackQuery):
    case_text = PORTFOLIO_CASES.get(callback.data, "Кейс не найден")
    try:
        await callback.message.edit_text(case_text, reply_markup=keyboards.back_to_portfolio_keyboard())
    except:
        await send_and_save_message(
            user_id=callback.from_user.id,
            text=case_text,
            reply_markup=keyboards.back_to_portfolio_keyboard()
        )
    await callback.answer()

# ===== ОБРАБОТКА НЕИЗВЕСТНЫХ СООБЩЕНИЙ =====
@dp.message()
async def unknown_message(message: types.Message):
    await send_and_save_message(
        user_id=message.from_user.id,
        text="Пожалуйста, используйте кнопки меню 👇",
        reply_markup=keyboards.main_menu()
    )

# ===== ЗАПУСК БОТА =====
async def main():
    logger.info("🚀 Запуск бота БотМастер.РФ...")
    logger.info(f"👤 Менеджер: @{config.config.MANAGER_USERNAME}")
    logger.info(f"🆔 Админ ID: {config.config.ADMIN_ID}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹ Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")