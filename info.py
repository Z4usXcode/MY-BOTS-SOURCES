import telebot
import aiohttp
import asyncio
import os
import time
from datetime import datetime

BOT_TOKEN = "8299457539:AAHJCDS75kSQpEyVRDSg3pOP8MGU3Mgonb4"

bot = telebot.TeleBot(BOT_TOKEN)

API_URL = "https://www.tiktok.com/passport/web/account/info/"


# ✅ TikTok API isteği
async def fetch_session(sessionid):
    cookies = {"sessionid": sessionid}
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile Safari/537.36)",
        "Referer": "https://www.tiktok.com/"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL, headers=headers, cookies=cookies) as resp:
                if resp.status != 200:
                    return {"error": f"HTTP Kod: {resp.status}"}

                try:
                    js = await resp.json()
                except:
                    text = await resp.text()
                    return {"error": "JSON okunamadı: " + text[:200]}

                data = js.get("data", {})

                return {
                    "session": sessionid,
                    "username": data.get("username"),
                    "screen": data.get("screen_name"),
                    "ctime": data.get("create_time"),
                    "email": "Evet ✅" if data.get("email") else "Hayır ❌",
                    "phone": "Evet ✅" if data.get("phone_number") else "Hayır ❌"
                }

        except Exception as e:
            return {"error": str(e)}


# ✅ Tek session sonuç gönderme
async def send_single(sessionid, chat_id):
    info = await fetch_session(sessionid)

    if "error" in info:
        bot.send_message(chat_id, f"❌ Hata: {info['error']}")
        return

    # Tarihi düzenle
    if info['ctime']:
        try:
            create_date = datetime.fromtimestamp(info['ctime']).strftime("%d.%m.%Y %H:%M:%S")
        except:
            create_date = "Bilinmiyor"
    else:
        create_date = "Bilinmiyor"

    msg = f"""
✅ SESSION SONUCU
------------------------
Session: {info['session']}

Username: {info['username']}
Screen Name: {info['screen']}
Create Time: {create_date}

Email Var mı? {info['email']}
Telefon Var mı? {info['phone']}
 LİNK : https://www.tiktok.com/@{info['username']}
"""

    bot.send_message(chat_id, msg)


# ✅ Çoklu session işleme
async def process_list(session_list, chat_id):
    for sess in session_list:
        await send_single(sess, chat_id)
        await asyncio.sleep(0.5)


# ✅ Text mesaj işle
@bot.message_handler(content_types=["text"])
def handle_text(msg):
    text = msg.text.strip()

    # Çoklu session
    if "\n" in text:
        sessions = [s.strip() for s in text.split("\n") if s.strip()]
        bot.send_message(msg.chat.id, f"📄 {len(sessions)} adet session bulundu, işleniyor...")
        asyncio.run(process_list(sessions, msg.chat.id))
        return

    # Tek session
    if len(text) >= 10:
        asyncio.run(send_single(text, msg.chat.id))
    else:
        bot.reply_to(msg, "❌ Geçersiz session ID.")


# ✅ TXT dosyasından session okuma
@bot.message_handler(content_types=['document'])
def handle_txt(msg):
    file_info = bot.get_file(msg.document.file_id)

    if not msg.document.file_name.endswith(".txt"):
        bot.reply_to(msg, "❌ Sadece .txt dosyası gönderebilirsin.")
        return

    dl = bot.download_file(file_info.file_path)

    path = "/sdcard/tiktok_sessions.txt"
    with open(path, "wb") as f:
        f.write(dl)

    bot.reply_to(msg, "📄 TXT alındı, işleniyor...")

    with open(path, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    asyncio.run(process_list(lines, msg.chat.id))


# ✅ Sonsuz polling — Pydroid için en stabil
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print("Polling hatası:", e)
        time.sleep(3)