import urllib.request
import json
import time
import urllib.parse

# --- НАСТРОЙКИ ---
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = "8014629371"
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y" # Вставь ключ из tonconsole.com
# -----------------

# Список коллекций (можно добавлять бесконечно)
COLLECTIONS = ["EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000"]

def send_msg(text, addr):
    links = (f"\n\n🔗 [GetGems](https://getgems.io/nft/{addr}) | "
             f"[Fragment](https://fragment.com/nft/{addr}) | "
             f"[Portals](https://portals.art/nft/{addr})")
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={MY_ID}&text={urllib.parse.quote(text + links)}&parse_mode=Markdown"
        urllib.request.urlopen(url)
    except: pass

print("🚀 БОТ НА TON_API ЗАПУЩЕН...")
seen_items = set()

while True:
    for col in COLLECTIONS:
        try:
            # Используем продвинутый метод TonAPI
            url = f"https://tonapi.io/v2/nfts/collections/{col}/items?limit=20"
            req = urllib.request.Request(url)
            req.add_header('Authorization', f'Bearer {API_KEY}')
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                items = data.get('nft_items', [])
                
                for item in items:
                    addr = item['address']
                    sale = item.get('sale')
                    
                    if sale and addr not in seen_items:
                        price_raw = int(sale['price']['value'])
                        price = price_raw / 10**9
                        
                        # Твой диапазон цен
                        if 3.0 <= price <= 10000.0:
                            name = item.get('metadata', {}).get('name', 'Telegram Gift')
                            msg = f"💎 *НОВЫЙ ЛОТ*\n📦 {name}\n💰 Цена: {price} TON"
                            send_msg(msg, addr)
                            seen_items.add(addr)
                            print(f"Нашел: {name} за {price}")

        except Exception as e:
            print(f"Сплю 10 сек... (Лимит или ошибка)")
            time.sleep(10)
    
    time.sleep(5) # Проверка каждые 5 секунд
