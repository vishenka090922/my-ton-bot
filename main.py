import urllib.request, json, time, urllib.parse

# ================= НАСТРОЙКИ =================
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = 8014629371 # Твой ID цифрами
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"
MAX_PRICE_GIFT = 10.0  
MAX_PRICE_NUM = 15.0   
MONO = {
    "Duck": "Yellow", "Skull": "Gray", "Santa": "Red",
    "Alien": "Green", "Lollipop": "Pink", "Ghost": "White", "Frog": "Green"
}
# =============================================

def send_tg(txt, photo=None):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/"
        url += "sendPhoto" if photo else "sendMessage"
        params = {'chat_id': MY_ID, 'parse_mode': 'HTML'}
        if photo: 
            params['photo'] = photo
            params['caption'] = txt
        else: 
            params['text'] = txt
        data = urllib.parse.urlencode(params).encode()
        urllib.request.urlopen(url, data=data)
    except Exception as e: print(f"Ош ТГ: {e}")

def is_cool_num(name):
    n = name.replace("+888","").replace(" ","")
    return any(str(i)*3 in n for i in range(10)) or n == n[::-1]

COLLECTIONS = {
    "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000": "GIFT",
    "EQAOZ_S_96p-In9V86XfM4S68-E9Y8T6T-6_6_6_6_6_6_6_6": "NUMBER"
}

done = set()
print("🎯 Охота...")
send_tg("✅ Бот в сети (90 строк)!")

while True:
    for col_addr, col_type in COLLECTIONS.items():
        try:
            link = f"https://tonapi.io/v2/nfts/collections/{col_addr}/items?limit=35"
            req = urllib.request.Request(link)
            req.add_header('Authorization', f'Bearer {API_KEY.strip()}')
            with urllib.request.urlopen(req) as r:
                items = json.loads(r.read().decode()).get('nft_items', [])
                for i in items:
                    addr = i.get('address')
                    sale = i.get('sale')
                    if not sale or addr in done: continue
                    
                    price = float(sale.get('price',{}).get('value',0))/10**9
                    meta = i.get('metadata', {})
                    name = meta.get('name', 'NFT')
                    img = meta.get('image', '')
                    attrs = meta.get('attributes', [])
                    m_url = sale.get('marketplace', {}).get('url', f"https://tonviewer.com/{addr}")
                    
                    find = False
                    reason = ""
                    if col_type == "GIFT":
                        bg = next((a['value'] for a in attrs if 'background' in a['trait_type'].lower()), "")
                        model = next((a['value'] for a in attrs if 'model' in a['trait_type'].lower()), "")
                        if model in MONO and MONO[model] == bg:
                            find = True
                            reason = f"🎨 <b>МОНОХРОМ ({model})</b>"
                        elif price <= MAX_PRICE_GIFT:
                            find = True
                            reason = "📉 <b>ДЕШЕВЫЙ ПОДАРОК</b>"
                    elif col_type == "NUMBER":
                        if is_cool_num(name):
                            find = True
                            reason = "🎰 <b>КРАСИВЫЙ НОМЕР</b>"
                        elif price <= MAX_PRICE_NUM:
                            find = True
                            reason = "📉 <b>ДЕШЕВЫЙ НОМЕР</b>"
                    if find:
                        msg = f"{reason}\n📦 {name}\n💰 {price} TON\n<a href='{m_url}'>КУПИТЬ</a>"
                        send_tg(msg, img)
                        done.add(addr)
        except Exception as e: print(f"Пауза: {e}")
    time.sleep(35)

# Строка 90 (пустой коммент для ровного счета)
