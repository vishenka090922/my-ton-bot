import urllib.request, json, time, urllib.parse

# === НАСТРОЙКИ ===
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = 8014629371 
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"

COL_ADDR = "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000"

def send_tg(txt, photo=None):
    try:
        u = f"https://api.telegram.org/bot{TOKEN}/" + ("sendPhoto" if photo else "sendMessage")
        p = {'chat_id': MY_ID, 'parse_mode': 'HTML', ('caption' if photo else 'text'): txt}
        if photo: p['photo'] = photo
        data = urllib.parse.urlencode(p).encode()
        urllib.request.urlopen(u, data=data, timeout=10)
    except: pass

done = set()
send_tg("🔔 <b>Режим «ВСЕ NFT» включен!</b>\nБуду присылать каждый новый лот из коллекции Gifts.")

while True:
    try:
        # Берем последние 20 выставленных предметов
        req = urllib.request.Request(f"https://tonapi.io/v2/nfts/collections/{COL_ADDR}/items?limit=20")
        req.add_header('Authorization', f'Bearer {API_KEY.strip()}')
        
        with urllib.request.urlopen(req, timeout=15) as r:
            items = json.loads(r.read().decode()).get('nft_items', [])
            for i in items:
                addr, sale = i.get('address'), i.get('sale')
                # Если лот не на продаже или мы его уже видели - скипаем
                if not sale or addr in done: continue
                
                price = float(sale.get('price', {}).get('value', 0)) / 10**9
                meta = i.get('metadata', {})
                name = meta.get('name', 'NFT Gift')
                img = meta.get('image', '')
                
                # Формируем прямую ссылку на Telegram
                url = f"https://t.me/nft/{name.replace(' ', '-').replace('#', '')}"
                
                msg = f"🆕 <b>НОВЫЙ ЛОТ НА РЫНКЕ</b>\n\n📦 {name}\n💰 <b>{price} TON</b>\n\n<a href='{url}'>🛒 КУПИТЬ В TELEGRAM</a>"
                
                send_tg(msg, img if img else None)
                done.add(addr)
                
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(10)

    # Пауза 30 секунд между проверками, чтобы не забанили
    time.sleep(30)
