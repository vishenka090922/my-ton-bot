import urllib.request
import json
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os

# ================= НАСТРОЙКИ =================
TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"  # <--- Вставь токен
MY_ID = "8014629371"           # <--- Вставь свой ID
API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y"    # <--- Вставь ключ с tonconsole.com
# ==============================================

# 1. ФЕЙКОВЫЙ СЕРВЕР ДЛЯ ОБМАНА RENDER
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"✅ Health check server started on port {port}")
    server.serve_forever()

# Запускаем "обманку" в фоновом потоке
threading.Thread(target=run_health_server, daemon=True).start()

# 2. ЛОГИКА ОХОТНИКА
COLLECTIONS = [
    "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000", # Обычные подарки
    "EQAs7O79Yf5qQ0r73fS907_6Y-f57f57f57f57f57f57f57"  # Лимитки
]

def send_telegram(text, addr):
    link = f"https://fragment.com/nft/{addr}"
    try:
        msg = f"{text}\n\n🔗 [ОТКРЫТЬ НА FRAGMENT]({link})"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = urllib.parse.urlencode({'chat_id': MY_ID, 'text': msg, 'parse_mode': 'Markdown'}).encode()
        urllib.request.urlopen(url, data=data)
    except Exception as e:
        print(f"Ошибка ТГ: {e}")

print("🚀 ОХОТА НАЧАЛАСЬ...")
processed = set()

while True:
    for col in COLLECTIONS:
        try:
            url = f"https://tonapi.io/v2/nfts/collections/{col}/items?limit=15"
            req = urllib.request.Request(url)
            req.add_header('Authorization', f'Bearer {API_KEY}')
            
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                for item in data.get('nft_items', []):
                    addr = item['address']
                    sale = item.get('sale')
                    if sale and addr not in processed:
                        price = int(sale['price']['value']) / 10**9
                        if 3.0 <= price <= 10000.0:
                            name = item.get('metadata', {}).get('name', 'Telegram Gift')
                            send_telegram(f"🔥 *ГЕМ НАЙДЕН!*\n📦 {name}\n💰 Цена: {price} TON", addr)
                            processed.add(addr)
        except:
            pass
    time.sleep(15) # Проверка каждые 15 секунд
