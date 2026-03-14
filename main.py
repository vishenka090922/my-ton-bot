import urllib.request
import json
import time
import urllib.parse

# --- ТВОИ ДАННЫЕ (ВСТАВЬ СЮДА СВОЕ) ---
TOKEN = "ТВОЙ_ТОКЕН_БОТА"
MY_ID = "ТВОЙ_ID"
# ----------------------------------------

# Список ID всех популярных коллекций подарков
COLLECTIONS = [
    "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000", # Стандартные
    "EQAs7O79Yf5qQ0r73fS907_6Y-f57f57f57f57f57f57f57", # Лимитированные
    # Можно добавлять еще адреса коллекций сюда
]

def send_msg(text, addr):
    # Добавляем все нужные тебе площадки в кнопки
    links = (
        f"\n\n🔗 *Где купить:*"
        f"\n🔹 [GetGems](https://getgems.io/nft/{addr})"
        f"\n🔹 [Fragment](https://fragment.com/nft/{addr})"
        f"\n🔹 [MRKT](https://mrkt.com/item/{addr})"
        f"\n🔹 [Portals](https://portals.art/nft/{addr})"
    )
    try:
        encoded_text = urllib.parse.quote(text + links)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={MY_ID}&text={encoded_text}&parse_mode=Markdown"
        urllib.request.urlopen(url)
    except Exception as e:
        print(f"Ошибка отправки в ТГ: {e}")

seen_items = set()
print("🚀 БОТ-ОХОТНИК ЗАПУЩЕН (ОХВАТ: ВСЕ ПЛОЩАДКИ)...")

while True:
    for collection_addr in COLLECTIONS:
        try:
            # Запрос к общему API блокчейна
            api_url = f"https://toncenter.com/api/v3/nft/items?collection_address={collection_addr}&limit=20"
            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read().decode())
                items = data.get('nft_items', [])
                
                for item in items:
                    sale = item.get('sale')
                    if sale and sale.get('price'):
                        # Переводим из нанотонов в TON
                        price = int(sale['price']) / 10**9
                        addr = item['address']
                        
                        # ТВОЙ НОВЫЙ ДИАПАЗОН ЦЕН
                        if 3.0 <= price <= 10000.0 and addr not in seen_items:
                            name = item.get('metadata', {}).get('name', 'Telegram Gift')
                            status = f"🔥 *НОВЫЙ ЛОТ НАЙДЕН*\n\n📦 *Название:* {name}\n💰 *Цена:* {price} TON"
                            
                            send_msg(status, addr)
                            print(f"Нашел: {name} за {price} TON")
                            seen_items.add(addr)
                            
        except Exception as e:
            # Если ошибка (например, лимит запросов), просто ждем
            pass
        
        time.sleep(2) # Небольшая пауза между коллекциями

    time.sleep(10) # Общая пауза перед новым кругом
