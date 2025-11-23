

import os
from pathlib import Path

def check_setup():
    print("🔍 Проверка установки бота...\n")
    
    base_dir = Path(__file__).parent
    print(f"📁 Базовая директория: {base_dir}\n")
    
    required_files = [
        'bot.py',
        'config.py',
        '.env',
        'requirements.txt',
    ]
    
    required_dirs = [
        'handlers',
        'keyboards',
        'locales',
        'utils',
    ]
    
    print("📄 Проверка файлов:")
    all_files_ok = True
    for file in required_files:
        file_path = base_dir / file
        exists = file_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
        if not exists:
            all_files_ok = False
    
    print("\n📁 Проверка папок:")
    all_dirs_ok = True
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        exists = dir_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {dir_name}/")
        if not exists:
            all_dirs_ok = False
    
    print("\n🔐 Проверка .env файла:")
    env_path = base_dir / '.env'
    if env_path.exists():
        print(f"  ✅ Файл существует: {env_path}")
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'BOT_TOKEN=' in content:
                print("  ✅ BOT_TOKEN найден")
            else:
                print("  ❌ BOT_TOKEN не найден")
                all_files_ok = False
            
            if 'ADMIN_ID=' in content:
                print("  ✅ ADMIN_ID найден")
            else:
                print("  ❌ ADMIN_ID не найден")
                all_files_ok = False
    else:
        print(f"  ❌ Файл не найден: {env_path}")
        all_files_ok = False
    
    print("\n📦 Проверка зависимостей:")
    try:
        import aiogram
        print(f"  ✅ aiogram {aiogram.__version__}")
    except ImportError:
        print("  ❌ aiogram не установлен")
        all_files_ok = False
    
    try:
        import dotenv
        print(f"  ✅ python-dotenv установлен")
    except ImportError:
        print("  ❌ python-dotenv не установлен")
        all_files_ok = False
    
    try:
        import aiofiles
        print(f"  ✅ aiofiles установлен")
    except ImportError:
        print("  ❌ aiofiles не установлен")
        all_files_ok = False
    
    print("\n" + "="*50)
    if all_files_ok and all_dirs_ok:
        print("✅ Все проверки пройдены! Можно запускать бота:")
        print("   python bot.py")
    else:
        print("❌ Обнаружены проблемы. Исправьте их перед запуском.")
        print("\n💡 Рекомендации:")
        if not all_files_ok:
            print("   1. Установите зависимости: pip install -r requirements.txt")
            print("   2. Проверьте файл .env")
        if not all_dirs_ok:
            print("   3. Убедитесь, что все папки на месте")
    print("="*50)

if __name__ == "__main__":
    check_setup()
