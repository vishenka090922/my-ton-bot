import urllib.request
import json
import time
import urllib.parse

# ================= НАСТРОЙКИ =================
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = 8014629371  # Твой ID цифрами (без кавычек)
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"

# Список коллекций (сейчас тут Телеграм Подарки)
COLLECTIONS = ["EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000"]

# Диапазон цен (от 0.1 до 100000 TON)
MIN_PRICE = 0.1 
MAX_PRICE = 100000.0
# =============================================

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {
            'chat_id': MY_ID,
            'text': text,
            'parse_mode': 'HTML'
        }
        data = urllib.parse.urlencode(params).encode()
        urllib.request.urlopen(url, data=data)
        print("✅ Сообщение в ТГ отправлено")
    except Exception as e:
        print(f"❌ Ошибка ТГ: {e}")

def check_market():
    processed = set()
    print("🚀 БОТ ЗАПУЩЕН! Начинаю охоту...")
    send_telegram("🤖 <b>Бот успешно запущен!</b>\nНачинаю сканирование рынка...")

    while True:
        print(f"🔎 Проверка рынка... ({time.strftime('%H:%M:%S')})")
        for col in COLLECTIONS:
            try:
                # Запрашиваем последние 50 предметов из коллекции
                url = f"https://tonapi.io/v2/nfts/collections/{col}/items?limit=50"
                req = urllib.request.Request(url)
                req.add_header('Authorization', f'Bearer {API_KEY}')
                
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode())
                    items = data.get('nft_items', [])

                    for item in items:
                        address = item.get('address')
                        
                        # Ищем цену в данных NFT
                        sale = item.get('sale')
                        if not sale:
                            continue
                            
                        raw_price = sale.get('price', {}).get('value')
                        if not raw_price:
                            continue
                            
                        # Переводим цену из нанотонов в TON
                        price = float(raw_price) / 10**9
                        
                        # Проверяем условия: новая ли покупка и подходит ли цена
                        if address not in processed:
                            if MIN_PRICE <= price <= MAX_PRICE:
                                name = item.get('metadata', {}).get('name', 'Без названия')
                                link = f"https://fragment.com/nft/{address}"
                                
                                msg = (f"🎁 <b>Найден лот!</b>\n\n"
                                       f"Название: {name}\n"
                                       f"Цена: <b>{price} TON</b>\n\n"
                                       f"<a href='{link}'>👉 Открыть на Fragment</a>")
                                
                                send_telegram(msg)
                                processed.add(address)
            
            except Exception as e:
                print(f"❌ Ошибка при запросе: {e}")
        
        # Пауза 15 секунд между проверками
        time.sleep(15)

if name == "main":
    check_market()
