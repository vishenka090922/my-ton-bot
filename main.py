import asyncio
import aiohttp
import json
import urllib.parse
from aiogram import Bot, Dispatcher

# ================= НАСТРОЙКИ =================
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = 8014629371 # Твой ID цифрами
TONAPI_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"

# Инициализируем бота максимально просто
bot = Bot(token=TOKEN)
dp = Dispatcher()
        "name": "Telegram Gifts", 
        "type": "nft", 
        "max_price": 50.0
    },
    "EQAOZ_S_96p-In9V86XfM4S68-E9Y8T6T-6_6_6_6_6_6_6_6": {
        "name": "Anonymous Numbers", 
        "type": "numbers", 
        "max_price": 20.0
    }
}
# =============================================

# Инициализация бота (aiogram 3.x)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def is_cool_number(name: str) -> bool:
    """
    Фильтрация крутых номеров +888.
    Ищет 4 одинаковые цифры подряд или зеркальные номера.
    """
    num = name.replace("+888", "").replace(" ", "")
    if len(num) < 8: 
        return False
    
    # 1. Поиск 4 одинаковых цифр подряд (например, 7777)
    if any(str(i)*4 in num for i in range(10)):
        return True
    
    # 2. Проверка на зеркалку (палиндром, читается одинаково туда и обратно)
    if num == num[::-1]:
        return True
        
    return False

def is_monochrome(attributes: list) -> tuple[bool, str]:
    """
    Логика проверки монохромов.
    Сравнивает атрибуты фона и объекта.
    Здесь находится заглушка (словарь MATCHES), куда ты можешь
    добавлять ID цветов или названия визуальных стилей.
    """
    # ЗАГЛУШКА ИД ЦВЕТОВ (Модель: Визуальный стиль/Фон)
    MATCHES = {
        "Duck": "Yellow",
        "Skull": "Gray",
        "Alien": "Green",
        "Lollipop": "Pink"
    }
    
    bg_color = ""
    model_name = ""
    
    for attr in attributes:
        trait = attr.get('trait_type', '').lower()
        val = attr.get('value', '')
        
        if 'background' in trait or 'backdrop' in trait:
            bg_color = val
        elif 'model' in trait or 'color' in trait:
            model_name = val
            
    # Если модель есть в нашей базе и ее фон совпадает с эталонным
    if model_name in MATCHES and MATCHES[model_name] == bg_color:
        return True, f"{model_name} + {bg_color}"
        
    return False, ""

async def fetch_market(session: aiohttp.ClientSession):
    """
    Асинхронная фоновая задача для мониторинга рынка.
    """
    processed = set()
    await bot.send_message(MY_ID, "🚀 <b>Асинхронный снайпер запущен!</b>\nМониторю все маркеты (GetGems, Fragment, Portal, MRKT).")
    
    while True:
        for col_address, config in COLLECTIONS.items():
            url = f"https://tonapi.io/v2/nfts/collections/{col_address}/items?limit=40"
            headers = {"Authorization": f"Bearer {TONAPI_KEY}"}
            
            try:
                async with session.get(url, headers=headers) as resp:
                    if resp.status != 200:
                        continue
                        
                    data = await resp.json()
                    items = data.get('nft_items', [])
                    
                    for item in items:
                        addr = item.get('address')
                        sale = item.get('sale')
                        
                        if not sale or addr in processed:
                            continue
                            
                        price = float(sale.get('price', {}).get('value', 0)) / 10**9
                        if price > config["max_price"]:
                            continue
                            
                        # Парсинг метаданныхmeta = item.get('metadata', {})
                        name = meta.get('name', 'Без названия')
                        image_url = meta.get('image', '')
                        attrs = meta.get('attributes', [])
                        
                        # Парсинг площадки
                        market = sale.get('marketplace', {})
                        m_name = market.get('name', 'Unknown Market').upper()
                        m_url = market.get('url', f"https://fragment.com/nft/{addr}")
                        
                        is_target = False
                        alert_reason = ""
                        
                        # --- ФИЛЬТРЫ ---
                        if config["type"] == "nft":
                            mono_check, mono_info = is_monochrome(attrs)
                            if mono_check:
                                is_target = True
                                alert_reason = f"🎨 <b>РЕДКИЙ МОНОХРОМ! ({mono_info})</b>"
                            elif price < 5.0: # Порог жесткой дешевизны
                                is_target = True
                                alert_reason = "📉 <b>ОЧЕНЬ НИЗКАЯ ЦЕНА!</b>"
                                
                        elif config["type"] == "numbers":
                            if is_cool_number(name):
                                is_target = True
                                alert_reason = "🎰 <b>КРУТОЙ НОМЕР!</b>"
                            elif price < 3.0:
                                is_target = True
                                alert_reason = "📉 <b>НОМЕР НИЖЕ РЫНКА!</b>"
                                
                        # --- ОТПРАВКА ---
                        if is_target:
                            processed.add(addr)
                            msg = (f"{alert_reason}\n\n"
                                   f"📦 Предмет: <b>{name}</b>\n"
                                   f"💰 Цена: <b>{price} TON</b>\n"
                                   f"🏬 Площадка: <code>{m_name}</code>\n\n"
                                   f"<a href='{m_url}'>👉 КУПИТЬ НА {m_name}</a>")
                            
                            # Если есть картинка, отправляем её вместе с текстом
                            if image_url:
                                await bot.send_photo(chat_id=MY_ID, photo=image_url, caption=msg)
                            else:
                                await bot.send_message(chat_id=MY_ID, text=msg)
                                
                            print(f"✅ Найден лот: {name} за {price} TON на {m_name}")
                            
            except Exception as e:
                print(f"❌ Ошибка парсинга: {e}")
                
        await asyncio.sleep(15) # Пауза между кругами

async def main():
    """
    Главная точка входа. Запускает aiohttp сессию и поллинг бота.
    """
    async with aiohttp.ClientSession() as session:
        # Запускаем фоновый мониторинг
        asyncio.create_task(fetch_market(session))
        # Запускаем самого бота
        await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
