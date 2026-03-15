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

done_ev = set()
send_tg("🚀 <b>Снайпер переведен в режим LIVE!</b>\nЛовлю моменты выставления лотов...")

while True:
    try:
        # Запрашиваем последние СОБЫТИЯ коллекции (самый быстрый метод)
        url = f"https://tonapi.io/v2/nfts/collections/{COL_ADDR}/history?limit=20"
        req = urllib.request.Request(url)
        req.add_header('Authorization', f'Bearer {API_KEY.strip()}')
        
        with urllib.request.urlopen(req, timeout=15) as r:
            events = json.loads(r.read().decode()).get('events', [])
            for ev in events:
                eid = ev.get('event_id')
                if eid in done_ev: continue
                
                for act in ev.get('actions', []):
                    # Нас интересует только начало продажи
                    if act.get('type') == 'NftSaleStart':
                        data = act.get('NftSaleStart', {})
                        nft = data.get('nft', {})
                        price = float(data.get('price', {}).get('value', 0)) / 10**9
                        
                        # Если цена в нашем диапазоне (или убери условие, чтобы видеть ВСЕ)
                        if price <= 150.0: 
                            meta = nft.get('metadata', {})
                            name = meta.get('name', 'NFT Gift')
                            img = meta.get('image', '')
                            
                            # Ссылка прямо в Telegram
                            clean_name = name.replace(" ", "-").replace("#", "")
                            tg_url = f"https://t.me/nft/{clean_name}"
                            
                            msg = f"⚡️ <b>ЛОТ ВЫСТАВЛЕН!</b>\n\n📦 {name}\n💰 <b>{price} TON</b>\n\n<a href='{tg_url}'>🛒 КУПИТЬ</a>"
                            send_tg(msg, img if img else None)
                
                done_ev.add(eid)
                # Чистим память, чтобы бот не тормозил
                if len(done_ev) > 500: done_ev.clear() 
                
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)

    time.sleep(5) # Проверка каждые 5 секунд
