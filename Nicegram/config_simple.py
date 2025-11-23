
BOT_TOKEN = "8370566284:AAEP4Xk6HGKWxNYCZOtWFosN2ckgmGEVovU"

ADMIN_ID = 7647578051

# Проверка конфигурации
if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    raise ValueError("❌ Установите BOT_TOKEN в файле config_simple.py")

if not ADMIN_ID or ADMIN_ID == 0:
    raise ValueError("❌ Установите ADMIN_ID в файле config_simple.py")

print(f"✅ Конфигурация загружена успешно")
print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
print(f"👤 Admin ID: {ADMIN_ID}")
