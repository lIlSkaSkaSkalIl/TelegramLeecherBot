# Telegram Uploader Bot v1.02,07
# Termasuk fitur: /m3u8 (dua langkah)

from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

from handlers.gdrive_handler import handle_gdrive
from handlers.direct_handler import handle_direct
from handlers.video_handler import handle_drlvideo
from handlers.gdvideo_handler import handle_gdvideo
from handlers.link_router import handle_link_input
from handlers.start_handler import handle_start
from handlers.help_handler import handle_help

from utils.state import user_state
from utility.video_utils import download_m3u8_video

import os

app = Client("uploader-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# =====================
# ✅ Command /start dan /help
# =====================
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await handle_start(client, message)

@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    await handle_help(client, message)

# =====================
# ☁️ GDrive & Direct Handlers
# =====================
@app.on_message(filters.command("gd"))
async def gdrive(client, message: Message):
    await handle_gdrive(client, message)

@app.on_message(filters.command("drl"))
async def direct(client, message: Message):
    await handle_direct(client, message)

@app.on_message(filters.command("drlvideo"))
async def drlvideo(client, message: Message):
    await handle_drlvideo(client, message)

@app.on_message(filters.command("gdvideo"))
async def gdvideo(client, message: Message):
    await handle_gdvideo(client, message)

# =====================
# 🎬 /m3u8 Download Handler
# =====================
@app.on_message(filters.command("m3u8") & filters.private)
async def m3u8_step_one(client, message: Message):
    await message.reply_text(
        "🎬 Silakan kirimkan link `.m3u8` Anda.\n\nContoh:\n`https://example.com/video/stream.m3u8`"
    )
    user_state[message.from_user.id] = "awaiting_m3u8_link"

@app.on_message(filters.text & filters.private)
async def m3u8_step_two(client, message: Message):
    user_id = message.from_user.id

    if user_state.get(user_id) == "awaiting_m3u8_link":
        m3u8_url = message.text.strip()
        if not m3u8_url.startswith("http") or ".m3u8" not in m3u8_url:
            await message.reply_text("❌ Link tidak valid. Pastikan itu adalah link `.m3u8`.")
            return

        await message.reply_text("⏳ Sedang mendownload video...")

        output_file = f"{user_id}_m3u8.mp4"
        status_msg = await message.reply_text("📥 Mulai mengunduh...")

        success = await download_m3u8_video(m3u8_url, output_file, status_msg, client)

        if not success or not os.path.exists(output_file):
            await status_msg.edit("❌ Gagal mendownload video.")
        else:
            await status_msg.edit("✅ Berhasil! Mengirimkan ke Telegram...")
            await client.send_video(chat_id=message.chat.id, video=output_file, caption="🎉 Selesai!")
            os.remove(output_file)

        user_state.pop(user_id, None)
        return  # Penting: hentikan eksekusi agar tidak diteruskan ke handler global

# =====================
# 🔁 Handler untuk input teks biasa
# =====================
@app.on_message(filters.text & ~filters.command(["start", "help", "gd", "drl", "drlvideo", "gdvideo", "m3u8"]))
async def link_input(client, message: Message):
    user_id = message.from_user.id

    # ⛔ Lewati jika sedang dalam mode m3u8
    if user_state.get(user_id) == "awaiting_m3u8_link":
        return

    await handle_link_input(client, message)

# =====================
# 🚀 Start Bot
# =====================
if __name__ == "__main__":
    print("✅ Bot siap berjalan!")
    app.run()
