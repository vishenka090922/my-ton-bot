import urllib.request, json, time, urllib.parse

TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"
MY_ID = 8014629371 # Сюда цифры без кавычек
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"
COL = "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000"

def send(txt):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        d = urllib.parse.urlencode({'chat_id':MY_ID,'text':txt,'parse_mode':'HTML'}).encode()
        urllib.request.urlopen(url, data=d)
    except: pass

print("🚀 СТАРТ...")
send("✅ Бот запущен!")
done = set()

while True:
    try:
        req = urllib.request.Request(f"https://tonapi.io/v2/nfts/collections/{COL}/items?limit=50")
        req.add_header('Authorization', f'Bearer {API_KEY}')
        with urllib.request.urlopen(req) as r:
            items = json.loads(r.read().decode()).get('nft_items', [])
            for i in items:
                addr = i.get('address')
                sale = i.get('sale')
                if sale and addr not in done:
                    price = float(sale.get('price',{}).get('value',0))/10**9
                    if 0.1 <= price <= 10000:
                        link = f"https://fragment.com/nft/{addr}"
                        send(f"🎁 <b>Лот:</b> {price} TON\n<a href='{link}'>Купить</a>")
                        done.add(addr)
    except Exception as e: print(f"Ошибка: {e}")
    time.sleep(20)
