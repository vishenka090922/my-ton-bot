const axios = require('axios');

const TOKEN = "8753959037:AAGqeA55UteuX6nc6i3W9lsqzT8IZ2quoi0";
const MY_ID = 8014629371;
const API_KEY = "AHN54X4JUOBUMUQAAAAFZM7B77G4OYWHOBW5XLORTEBJXXD2HYJQVNDF5KLSDUUHSLFFN5Y";
const COL_ADDR = "EQCA14o1-V_6V7IInW57S7x1yX4Kde000000000000000000";

let doneEv = new Set();

async function sendTg(txt, img) {
    const method = img ? 'sendPhoto' : 'sendMessage';
    const url = https://api.telegram.org/bot${TOKEN}/${method};
    const data = img ? { chat_id: MY_ID, photo: img, caption: txt, parse_mode: 'HTML' } 
                     : { chat_id: MY_ID, text: txt, parse_mode: 'HTML' };
    try { await axios.post(url, data); } catch (e) { console.error("TG Error"); }
}

async function scan() {
    try {
        const res = await axios.get(https://tonapi.io/v2/nfts/collections/${COL_ADDR}/history?limit=20, {
            headers: { 'Authorization': Bearer ${API_KEY} }
        });

        const events = res.data.events || [];
        for (const ev of events) {
            if (doneEv.has(ev.event_id)) continue;

            ev.actions.forEach(act => {
                if (act.type === 'NftSaleStart') {
                    const data = act.NftSaleStart;
                    const price = data.price.value / 10**9;
                    
                    if (price <= 150) { // Лимит для теста
                        const name = data.nft.metadata.name || "NFT Gift";
                        const img = data.nft.metadata.image;
                        const url = https://t.me/nft/${name.replace(/\s+/g, '-').replace('#', '')};
                        
                        const msg = ⚡️ <b>NODE.JS SPEED: ЛОТ ВЫСТАВЛЕН!</b>\n\n📦 ${name}\n💰 <b>${price} TON</b>\n\n<a href='${url}'>🛒 КУПИТЬ</a>;
                        sendTg(msg, img);
                    }
                }
            });
            doneEv.add(ev.event_id);
        }
        if (doneEv.size > 1000) doneEv.clear();
    } catch (e) { console.error("Scan error"); }
}

console.log("🚀 Node.js Снайпер запущен!");
sendTg("🚀 <b>Node.js Снайпер запущен!</b>\nТеперь работаем на максимальной скорости.");

// Проверка каждые 4 секунды (Node.js это делает очень легко)
setInterval(scan, 4000);
