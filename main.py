import urllib.request
import json
import time
import urllib.parse

# --- ТВОИ ДАННЫЕ (ОБЯЗАТЕЛЬНО ЗАПОЛНИ) ---
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = "8014629371"
# ----------------------------------------

COLLECTION = "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000"

def send_msg(text, addr):
    links = (f"\n\n🔹 [GetGems](https://getgems.io/nft/{addr})\n"
             f"🔹 [MRKT](https://mrkt.com/item/{addr})")
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={MY_ID}&text={urllib.parse.quote(text + links)}&parse_mode=Markdown"
        urllib.request.urlopen(url)
    except:
        pass

seen_items = set()
print("🚀 БОТ ЗАПУЩЕН И ИЩЕТ ГЕМЫ...")

while True:
    try:
        # Используем публичный API Toncenter
        api_url = f"https://toncenter.com/api/v3/nft/items?collection_address={COLLECTION}&limit=15"
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            items = data.get('nft_items', [])
            
            for item in items:
                sale = item.get('sale')
                if sale and sale.get('price'):
                    price = int(sale['price']) / 10**9
                    addr = item['address']
                    
                    if 4.0 <= price <= 8.0 and addr not in seen_items:
                        name = item.get('metadata', {}).get('name', 'Telegram Gift')
                        status = f"✅ НАЙДЕН ЛОТ\n📦 {name}\n💰 Цена: {price} TON"
                        send_msg(status, addr)
                        print(f"Нашел лот: {name}")
                        seen_items.add(addr)
    except Exception as e:
        print("Сканирую блокчейн...")
    
    time.sleep(15) # Пауза чтобы не забанили
