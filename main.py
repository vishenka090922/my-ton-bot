import urllib.request, json, time, urllib.parse

# === НАСТРОЙКИ (Впиши свои данные) ===
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = 8014629371  # Твой ID
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"
MIN_P, MAX_P = 4.0, 80.0
# =====================================

# Полный список монохромов (Модель: Цвет фона)
MONO = {
    "Duck": "Yellow", "Skull": "Gray", "Santa": "Red", 
    "Alien": "Green", "Lollipop": "Pink", "Ghost": "White", 
    "Frog": "Green", "Dog": "Brown", "Pumpkin": "Orange",
    "Cactus": "Green", "Pizza": "Yellow", "Popcorn": "Yellow",
    "Diamond": "Blue", "Heart": "Red", "Cherry": "Red",
    "Melon": "Green", "Panda": "White", "Penguin": "Blue",
    "Owl": "Brown", "Pig": "Pink", "Unicorn": "Pink",
    "Cat": "Gray", "Dragon": "Red", "Bear": "Brown"
}

# Основные коллекции: Подарки, Номера, Юзернеймы
COLLECTIONS = {
    "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000": "GIFT",
    "EQAOZ_S_96p-In9V86XfM4S68-E9Y8T6T-6_6_6_6_6_6_6_6": "NUMBER",
    "EQC61_4vH_l_u_p-In9V86XfM4S68-E9Y8T6T-6_6_6_6_6_6": "NAME"
}

def send_tg(txt, photo=None):
    try:
        u = f"https://api.telegram.org/bot{TOKEN}/" + ("sendPhoto" if photo else "sendMessage")
        p = {'chat_id': MY_ID, 'parse_mode': 'HTML'}
        if photo: p['photo'], p['caption'] = photo, txt
        else: p['text'] = txt
        data = urllib.parse.urlencode(p).encode()
        urllib.request.urlopen(u, data=data, timeout=10)
    except: pass

done = set()
last_ping = time.time()
send_tg("🚀 <b>Снайпер запущен!</b>\nМониторю Подарки, Номера и Имена.")

while True:
    # Пинг раз в 15 минут, чтобы знать, что бот жив
    if time.time() - last_ping > 900:
        send_tg("🕵️ Снайпер в засаде, жду выгодный лот...")
        last_ping = time.time()

    for addr_col, c_type in COLLECTIONS.items():
        try:
            api_url = f"https://tonapi.io/v2/nfts/collections/{addr_col}/items?limit=40"
            req = urllib.request.Request(api_url)
            # Очистка ключа от лишних пробелов
            req.add_header('Authorization', f'Bearer {API_KEY.strip()}')
            req.add_header('Accept', 'application/json')
            
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
                items = data.get('nft_items', [])
                
                for i in items:
                    addr = i.get('address')
                    sale = i.get('sale')
                    if not sale or addr in done: continue
                    
                    price = float(sale.get('price', {}).get('value', 0)) / 10**9
                    meta = i.get('metadata', {})
                    name = meta.get('name', 'NFT')
                    img = meta.get('image', '')
                    attrs = meta.get('attributes', [])
                    m_url = sale.get('marketplace', {}).get('url', f"https://tonviewer.com/{addr}")
                    
                    find, res_msg = False, ""

                    # ЛОГИКА ДЛЯ ПОДАРКОВ (Монохромы + Цена)
                    if c_type == "GIFT":
                        bg = next((a['value'] for a in attrs if 'background' in a['trait_type'].lower()), "")
                        mod = next((a['value'] for a in attrs if 'model' in a['trait_type'].lower()), "")
                        
                        # Проверка на монохром
                        if mod in MONO and MONO[mod].lower() == bg.lower():
                            find, res_msg = True, f"🎨 <b>МОНОХРОМ ({mod})</b>"
                        # Проверка просто на низкую цену
                        elif MIN_P <= price <= MAX_P:
                            find, res_msg = True, "💰 <b>ХАЛЯВА (GIFT)</b>"

                    # ЛОГИКА ДЛЯ НОМЕРОВ И ИМЕН (Только цена)
                    elif c_type in ["NUMBER", "NAME"]:
                        if MIN_P <= price <= MAX_P:
                            tag = "НОМЕР" if c_type == "NUMBER" else "ИМЯ"
                            find, res_msg = True, f"💎 <b>ВЫГОДНЫЙ {tag}</b>"if find:
                        msg = f"{res_msg}\n📦 {name}\n💰 <b>{price} TON</b>\n\n<a href='{m_url}'>🛒 КУПИТЬ НА МАРКЕТЕ</a>"
                        send_tg(msg, img if img else None)
                        done.add(addr)

            time.sleep(8) # Пауза между коллекциями
        except Exception as e:
            print(f"Ошибка в цикле: {e}")
            time.sleep(15)

    time.sleep(60) # Пауза перед новым кругом
