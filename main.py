import urllib.request
import json
import time
import urllib.parse
import os

# --- ТВОИ ДАННЫЕ (ПРОВЕРЬ ИХ 100 РАЗ) ---
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = "8014629371"  # Должно быть числом, например 12345678
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"
# ---------------------------------------

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = urllib.parse.urlencode({'chat_id': MY_ID, 'text': text}).encode()
        urllib.request.urlopen(url, data=data)
        print("✅ Сообщение в Телеграм отправлено!")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

print("🚀 СТАРТ БОТА...")
send_telegram("🤖 Бот запущен и видит твой ID!")

COLLECTIONS = ["EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000"]

while True:
    print("🔎 ПРОВЕРЯЮ РЫНОК...") # Эта надпись ДОЛЖНА быть в логах
    for col in COLLECTIONS:
        try:
            url = f"https://tonapi.io/v2/nfts/collections/{col}/items?limit=10"
            req = urllib.request.Request(url)
            req.add_header('Authorization', f'Bearer {API_KEY}')
            
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                # Просто для теста выведем в лог, что мы что-то получили
                items_count = len(data.get('nft_items', []))
                print(f"--- Получено {items_count} предметов из коллекции ---")
        except Exception as e:
            print(f"❌ Ошибка API: {e}")
            
    time.sleep(15)
