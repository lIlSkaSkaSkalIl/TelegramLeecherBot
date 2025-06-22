# Telegram Uploader Bot v1.02,06
# Versi langsung jalan - dari link → upload ke chat

from pyrogram import Client, filters
from pyrogram.types import Message
from handlers.download_handler import process_link
import os

# Ambil kredensial dari environment variable (Colab, Replit, atau VPS)
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Inisialisasi Pyrogram Bot
app = Client("uploader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Perintah /start
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply(
        "👋 Halo!\n\n"
        "Saya adalah bot yang dapat mengunduh file dari direct download link dan mengunggahnya kembali ke Telegram.\n\n"
        "📎 Kirimkan saja link seperti:\n"
        "`https://example.com/file.zip`\n\n"
        "Saya akan mengurus sisanya. Selamat mencoba!"
    )

# Handler untuk menerima semua link langsung
@app.on_message(filters.text & filters.private)
async def handle_link(client, message: Message):
    await process_link(client, message)

# Jalankan bot
app.run()
