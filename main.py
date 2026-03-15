import urllib.request, json, time, urllib.parse

# ================= НАСТРОЙКИ =================
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = 8014629371  # Твой ID
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"

# Цены и Монохромы
MAX_GIFT_PRICE = 60.0
MONO_LIST = {
    "Duck": "Yellow", "Skull": "Gray", "Santa": "Red", 
    "Alien": "Green", "Lollipop": "Pink", "Ghost": "White"
}

COL_GIFTS = "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000"
COL_NUMS = "EQAOZ_S_96p-In9V86XfM4S68-E9Y8T6T-6_6_6_6_6_6_6_6"
# =============================================

def send_tg(txt, photo=None):
    try:
        # Если есть фото, отправляем его, если нет — просто текст
        if photo:
            url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            params = {'chat_id': MY_ID, 'photo': photo, 'caption': txt, 'parse_mode': 'HTML'}
        else:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            params = {'chat_id': MY_ID, 'text': txt, 'parse_mode': 'HTML'}
        
        data = urllib.parse.urlencode(params).encode()
        urllib.request.urlopen(url, data=data)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def check_cool_num(name):
    n = name.replace("+888","").replace(" ","")
    return any(str(i)*3 in n for i in range(10))

print("🚀 СНАЙПЕР ЗАПУЩЕН (БЕЗ БИБЛИОТЕК)...")
send_tg("✅ <b>Снайпер активен!</b>\nРаботаю на прямых запросах.")
done = set()

while True:
    for col in [COL_GIFTS, COL_NUMS]:
        try:
            req = urllib.request.Request(f"https://tonapi.io/v2/nfts/collections/{col}/items?limit=40")
            req.add_header('Authorization', f'Bearer {API_KEY}')
            with urllib.request.urlopen(req) as r:
                items = json.loads(r.read().decode()).get('nft_items', [])
                for i in items:
                    addr = i.get('address')
                    sale = i.get('sale')
                    meta = i.get('metadata', {})
                    if sale and addr not in done:
                        price = float(sale.get('price',{}).get('value',0))/10**9
                        if price > 1000: continue # Защита от мусора
                        
                        name = meta.get('name', '')
                        img = meta.get('image', '')
                        attrs = meta.get('attributes', [])
                        
                        m_name = sale.get('marketplace', {}).get('name', 'MARKET').upper()
                        m_url = sale.get('marketplace', {}).get('url', f"https://fragment.com/nft/{addr}")
                        
                        is_target = False
                        msg_type = ""

                        if col == COL_GIFTS and price <= MAX_GIFT_PRICE:
                            bg = next((a['value'] for a in attrs if 'background' in a['trait_type'].lower()), "")
                            model = next((a['value'] for a in attrs if 'model' in a['trait_type'].lower()), "")
                            if model in MONO_LIST and MONO_LIST[model] == bg:
                                is_target = True
                                msg_type = f"🎨 <b>МОНОХРОМ! ({model})</b>"
                            elif price < 3.0:
                                is_target = True
                                msg_type = "📉 <b>ДЕШЕВЫЙ ПОДАРОК!</b>"

                        elif col == COL_NUMS and price <= 20.0:
                            if check_cool_num(name):
                                is_target = True
                                msg_type = "🎰 <b>КРУТОЙ НОМЕР!</b>"

                        if is_target:
                            text = (f"{msg_type}\n\n📦 {name}\n💰 Цена: <b>{price} TON</b>\n"
                                    f"🏬 Маркет: {m_name}\n\n<a href='{m_url}'>👉 КУПИТЬ</a>")
                            send_tg(text, img)
                            done.add(addr)
        except Exception as e:
            print(f"Ошибка круга: {e}")
    time.sleep(15)
