const axios = require('axios');

// === ТВОИ ДАННЫЕ (ВСТАВЬ ВНУТРЬ КАВЫЧЕК) ===
const TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0"; 
const MY_ID = 8014629371; // ПИШИ ПРОСТО ЦИФРАМИ БЕЗ КАВЫЧЕК
const API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y";

const MAX_P = 150.0; 
const COL_ADDR = "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000";
let doneEv = new Set();

async function sendTg(txt, img) {
    try {
        const method = img ? 'sendPhoto' : 'sendMessage';
        // ВАЖНО: Тут стоят косые кавычки (клавиша Ё)
        const url = https://api.telegram.org/bot${TOKEN}/${method};
        
        const params = img ? { chat_id: MY_ID, photo: img, caption: txt, parse_mode: 'HTML' } 
                         : { chat_id: MY_ID, text: txt, parse_mode: 'HTML' };
        
        await axios.post(url, params);
        console.log("✅ Сообщение отправлено");
    } catch (e) {
        console.error("❌ Ошибка ТГ:", e.response ? e.response.data.description : e.message);
    }
}

async function scan() {
    try {
        const res = await axios.get(https://tonapi.io/v2/nfts/collections/${COL_ADDR}/history?limit=15, {
            headers: { 'Authorization': Bearer ${API_KEY.trim()} }
        });

        const events = res.data.events || [];
        for (const ev of events) {
            if (doneEv.has(ev.event_id)) continue;
            
            if (ev.actions) {
                for (const act of ev.actions) {
                    if (act.type === 'NftSaleStart') {
                        const data = act.NftSaleStart;
                        const price = data.price.value / 1e9;
                        
                        if (price <= MAX_P) {
                            const name = data.nft.metadata.name || "NFT Gift";
                            const img = data.nft.metadata.image;
                            // Тут тоже косые кавычки (клавиша Ё)
                            const tgUrl = https://t.me/nft/${name.replace(/\s+/g, '-').replace('#', '')};
                            
                            const msg = ⚡️ <b>ЛОТ ВЫСТАВЛЕН!</b>\n\n📦 ${name}\n💰 <b>${price} TON</b>\n\n<a href='${tgUrl}'>🛒 КУПИТЬ</a>;
                            await sendTg(msg, img);
                        }
                    }
                }
            }
            doneEv.add(ev.event_id);
        }
        if (doneEv.size > 1000) doneEv.clear();
    } catch (e) {
        console.error("⚠ Ошибка сканирования:", e.message);
    }
}

console.log("🚀 Снайпер запущен!");
// Тестовое сообщение при старте
sendTg("🚀 <b>Node.js Снайпер LIVE!</b>\nЕсли видишь это — бот работает.");

// Проверка каждые 5 секунд
setInterval(scan, 5000);
