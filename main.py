import urllib.request, json, time, urllib.parse

# === НАСТРОЙКИ ===
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = 8014629371 
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"
MIN_P, MAX_P = 4.0, 80.0

MONO = {
    "Duck":"Yellow","Skull":"Gray","Santa":"Red","Alien":"Green","Lollipop":"Pink",
    "Ghost":"White","Frog":"Green","Dog":"Brown","Pumpkin":"Orange","Cactus":"Green",
    "Pizza":"Yellow","Popcorn":"Yellow","Diamond":"Blue","Heart":"Red","Cherry":"Red",
    "Melon":"Green","Panda":"White","Penguin":"Blue","Owl":"Brown","Pig":"Pink",
    "Unicorn":"Pink","Cat":"Gray","Dragon":"Red","Bear":"Brown"
}
COLS = {
    "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000": "GIFT",
    "EQAOZ_S_96p-In9V86XfM4S68-E9Y8T6T-6_6_6_6_6_6_6_6": "NUM",
    "EQC61_4vH_l_u_p-In9V86XfM4S68-E9Y8T6T-6_6_6_6_6_6": "NAME"
}

def send_tg(txt, photo=None):
    try:
        u = f"https://api.telegram.org/bot{TOKEN}/" + ("sendPhoto" if photo else "sendMessage")
        p = {'chat_id': MY_ID, 'parse_mode': 'HTML', ('caption' if photo else 'text'): txt}
        if photo: p['photo'] = photo
        data = urllib.parse.urlencode(p).encode()
        urllib.request.urlopen(u, data=data, timeout=10)
    except: pass

done, last_p = set(), time.time()
send_tg("🚀 <b>Снайпер запущен!</b> (Gifts/Nums/Names)")

while True:
    if time.time() - last_p > 900:
        send_tg("🕵️ Снайпер в засаде...")
        last_p = time.time()
    for addr_col, c_type in COLS.items():
        try:
            req = urllib.request.Request(f"https://tonapi.io/v2/nfts/collections/{addr_col}/items?limit=40")
            req.add_header('Authorization', f'Bearer {API_KEY.strip()}')
            with urllib.request.urlopen(req, timeout=15) as r:
                items = json.loads(r.read().decode()).get('nft_items', [])
                for i in items:
                    addr = i.get('address')
                    sale = i.get('sale')
                    if not sale or addr in done: continue
                    price = float(sale.get('price', {}).get('value', 0)) / 10**9
                    meta = i.get('metadata', {})
                    attrs = meta.get('attributes', [])
                    find, res = False, ""
                    if c_type == "GIFT":
                        bg = next((a['value'] for a in attrs if 'background' in a['trait_type'].lower()), "")
                        mod = next((a['value'] for a in attrs if 'model' in a['trait_type'].lower()), "")
                        if mod in MONO and MONO[mod].lower() == bg.lower():
                            find, res = True, f"🎨 <b>МОНОХРОМ ({mod})</b>"
                        elif MIN_P <= price <= MAX_P:
                            find, res = True, "💰 <b>ХАЛЯВА (GIFT)</b>"
                    elif MIN_P <= price <= MAX_P:
                        find, res = True, f"💎 <b>ВЫГОДНЫЙ {c_type}</b>"
                    if find:
                        m_url = sale.get('marketplace', {}).get('url', f"https://tonviewer.com/{addr}")
                        msg = f"{res}\n📦 {meta.get('name')}\n💰 <b>{price} TON</b>\n<a href='{m_url}'>🛒 КУПИТЬ</a>"
                        send_tg(msg, meta.get('image'))
                        done.add(addr)
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}"); time.sleep(20)
    time.sleep(60)
