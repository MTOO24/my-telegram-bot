import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class Config:
    # Токен берется ТОЛЬКО из переменных окружения
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    MANAGER_USERNAME = os.environ.get('MANAGER_USERNAME', 'zamjk')
    ADMIN_ID = int(os.environ.get('ADMIN_ID', 8366233854))
    
    @classmethod
    def validate(cls):
        """Проверяем, что токен установлен"""
        if not cls.BOT_TOKEN:
            raise ValueError("❌ ОШИБКА: BOT_TOKEN не найден в .env файле!")
        if cls.BOT_TOKEN == "ВСТАВЬТЕ_СЮДА_ВАШ_ТОКЕН_БОТА":
            raise ValueError("❌ ОШИБКА: Замените 'ВСТАВЬТЕ_СЮДА_ВАШ_ТОКЕН_БОТА' на реальный токен в .env файле!")
        return True

config = Config()