const axios = require('axios');

// ================= НАСТРОЙКИ =================
const TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"; 
const MY_ID = 8014629371; // Твой ID цифрами
const API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y";

const MAX_PRICE = 150.0; // Макс. цена для уведомления
const COL_ADDR = "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000";
// =============================================

let doneEv = new Set();

async function sendTg(txt, img) {
    try {
        const method = img ? 'sendPhoto' : 'sendMessage';
        // Соединяем строку через плюсы, чтобы избежать ошибок с кавычками
        const url = 'https://api.telegram.org/bot' + TOKEN + '/' + method;
        
        const params = {
            chat_id: MY_ID,
            parse_mode: 'HTML'
        };

        if (img) {
            params.photo = img;
            params.caption = txt;
        } else {
            params.text = txt;
        }

        await axios.post(url, params);
        console.log("✅ Сообщение отправлено в Telegram");
    } catch (e) {
        console.error("❌ Ошибка Telegram:", e.response ? e.response.data.description : e.message);
    }
}

async function scan() {
    try {
        const url = 'https://tonapi.io/v2/nfts/collections/' + COL_ADDR + '/history?limit=15';
        const res = await axios.get(url, {
            headers: { 'Authorization': 'Bearer ' + API_KEY.trim() }
        });

        const events = res.data.events || [];
        for (const ev of events) {
            if (doneEv.has(ev.event_id)) continue;

            if (ev.actions) {
                ev.actions.forEach(act => {
                    if (act.type === 'NftSaleStart') {
                        const data = act.NftSaleStart;
                        const price = data.price.value / 1000000000;
                        
                        if (price <= MAX_PRICE) {
                            const name = data.nft.metadata.name || "NFT Gift";
                            const img = data.nft.metadata.image;
                            
                            // Создаем ссылку без лишних символов
                            const cleanName = name.split(' ').join('-').split('#').join('');
                            const buyUrl = 'https://t.me/nft/' + cleanName;
                            
                            const msg = '⚡️ <b>ЛОТ ВЫСТАВЛЕН!</b>\n\n' +
                                        '📦 ' + name + '\n' +
                                        '💰 <b>' + price + ' TON</b>\n\n' +
                                        '<a href="' + buyUrl + '">🛒 КУПИТЬ</a>';
                            
                            sendTg(msg, img);
                        }
                    }
                });
            }
            doneEv.add(ev.event_id);
        }
        // Очистка памяти
        if (doneEv.size > 1000) doneEv.clear();
    } catch (e) {
        console.error("⚠ Ошибка сканирования:", e.message);
    }
}

console.log("🚀 Снайпер запущен и работает!");

// Приветствие при старте
sendTg("🚀 <b>Node.js Снайпер LIVE!</b>\nЯ на связи и мониторю рынок.");

// Запуск цикла каждые 5 секунд
setInterval(scan, 5000);
