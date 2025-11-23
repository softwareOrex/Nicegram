import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = ""

ADMIN_ID =  #тут ваш айди

IMAGES_DIR = Path(__file__).parent / 'images'
MAIN_MENU_PHOTO = os.getenv('MAIN_MENU_PHOTO', str(IMAGES_DIR / '/storage/emulated/0/Nicegram/images/Nicegram.jpg'))
INSTRUCTION_PHOTO = os.getenv('INSTRUCTION_PHOTO', str(IMAGES_DIR / '/storage/emulated/0/Nicegram/images/Nicegram.jpg'))

if not BOT_TOKEN:
    print(f"❌ Ошибка: Файл .env должен находиться здесь: {env_path}")
    print(f"📁 Текущая директория: {Path(__file__).parent}")
    print(f"📄 Файл .env существует: {env_path.exists()}")
    if env_path.exists():
        print(f"📝 Содержимое .env:")
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.strip():
                print("Файл не пустой, но BOT_TOKEN не найден")
            else:
                print("Файл пустой!")
    raise ValueError("BOT_TOKEN не установлен в файле")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID не установлен в файле")

print(f"✅ Конфигурация загружена успешно")
print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
print(f"👤 Admin ID: {ADMIN_ID}")
