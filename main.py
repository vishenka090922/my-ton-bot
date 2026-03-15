import urllib.request, json, time, urllib.parse

# ================= НАСТРОЙКИ (ВНИМАТЕЛЬНО!) =================
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"  # Токен от BotFather
MY_ID = 8014629371           # Твой ID (только цифры, без кавычек!)
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y" # Ключ от tonapi.io
# ============================================================

# Чистим ключи от случайных пробелов
TOKEN = TOKEN.strip()
API_KEY = API_KEY.strip()

def send_tg(txt, photo=None):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/"
        url += "sendPhoto" if photo else "sendMessage"
        params = {'chat_id': MY_ID, 'parse_mode': 'HTML'}
        if photo: params['photo'] = photo; params['caption'] = txt
        else: params['text'] = txt
        data = urllib.parse.urlencode(params).encode()
        urllib.request.urlopen(url, data=data)
    except Exception as e:
        print(f"Ошибка Telegram: {e}")

print("🚀 ПРОВЕРКА ЗАПУЩЕНА...")
send_tg("🚀 <b>Снайпер запущен и проверяет настройки!</b>")

# Список коллекций
COLS = [
    "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000", # Gifts
    "EQAOZ_S_96p-In9V86XfM4S68-E9Y8T6T-6_6_6_6_6_6_6_6"  # Numbers
]

done = set()

while True:
    for col in COLS:
        try:
            link = f"https://tonapi.io/v2/nfts/collections/{col}/items?limit=30"
            req = urllib.request.Request(link)
            req.add_header('Authorization', f'Bearer {API_KEY}')
            
            with urllib.request.urlopen(req) as r:
                res = json.loads(r.read().decode())
                items = res.get('nft_items', [])
                print(f"📡 Проверяю коллекцию... Нашел {len(items)} предметов")
                
                for i in items:
                    addr = i.get('address')
                    sale = i.get('sale')
                    if sale and addr not in done:
                        # Логика уведомления (упрощенно для теста)
                        price = float(sale.get('price',{}).get('value',0))/10**9
                        name = i.get('metadata', {}).get('name', 'NFT')
                        if price < 500: # Пока ловим всё дешевле 500 TON для проверки
                            send_tg(f"💎 <b>Найден лот!</b>\n{name}\nЦена: {price} TON")
                            done.add(addr)
        except Exception as e:
            print(f"❌ Ошибка на коллекции {col[:10]}: {e}")
            
    time.sleep(20)
